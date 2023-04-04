import { ref, computed } from 'vue'
import vuetify from '@/services/vuetify'

import { useFormatHelpers, hexToRGB } from '../../../services/composables'

export function useChartConfig ({
  chartType,
  labels,
  datasets, 
  title,
  xLabel,
  xTickFormat,
  xTickPrefix,
  xTickSuffix,
  xTickFormatOptions,
  xScaleOptions,
  yLabel,
  yTickFormat,
  yTickPrefix,
  yTickSuffix,
  yTickFormatOptions,
  options,
  }){
  // ChartOptions setup
  const format = useFormatHelpers()
  const colors = [
    '#3a5ba9', // primary variant 1
    '#80ba56', // secondary
    '#6b88cc', // primary variant 1 lighten 30%
    '#cde4bd', // secondary lighten 30%
    '#adbde3', // primary variant 1 lighten 60%
    '#a6cf89', // secondary lighten 60%
  ]
  const tickCallback = (value, index, ticks, tickFormat, tickPrefix, tickSuffix, formatOptions) => {
    if (tickFormat.value) {
      return format[tickFormat.value](value, formatOptions.value)
    }
    else
      return tickPrefix.value + format.number(value) + tickSuffix.value
  }
  const xTickCallback = computed(() => {
    if (xScaleOptions.value?.type === 'time')
      return (tick) => new Date(tick).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }).split(' ')
    else if (chartType.value === 'line')
      return (value, index, ticks) => tickCallback(value, index, ticks, xTickFormat, xTickPrefix, xTickSuffix, xTickFormatOptions)
    else
      return (tick) => tick
  })
  const yTickCallback = computed(() => {
    return (value, index, ticks) => tickCallback(value, index, ticks, yTickFormat, yTickPrefix, yTickSuffix, yTickFormatOptions)
  })
  
  const axisLabelMaker = (label) => {
    if (label?.value)
      return {
        display: true, 
        text: label.value,
        align: 'center',
      }
    else
      return {display: false}
  }
  const xAxisLabel = computed(() => axisLabelMaker(xLabel))
  const yAxisLabel = computed(() => axisLabelMaker(yLabel))
  var elements = computed(() => {
    if (chartType.value === 'scatter')
      return {
        point: {
          pointStyle: 'circle',
          radius: 1,
          // borderWidth: 1,
        }
      }
    else
      return {point: {radius: 0}}
  })

  const chartOptions = computed(() => {
    var basePlugins = {
      title: {
        display: true,
        text: () => title.value,
        color: '#ffffffde',
        font: {
          size: 16,
          weight: 'normal'
        }
      },
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          usePointStyle: true,
          pointStyleWidth: 12,
          boxHeight: 8,
        }
      },
    }
    var plugins = Object.assign(basePlugins, options.value?.plugins)
    delete options.value?.plugins

    var baseOptions = {
      responsive: true,
      plugins,
      elements: elements.value,
      scales: {
        x: {
          title: xAxisLabel.value,
          border: {
            color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
          },
          grid: {
            display: false,
          },
          ticks: {
            callback: xTickCallback.value
          },
          ...xScaleOptions.value,
        },
        y: {
          beginAtZero: true,
          title: yAxisLabel.value,
          border: {
            color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
          },
          grid: {
            display: false,
          },
          ticks: { 
            callback: yTickCallback.value,
          }
        }
      }
    }
    return Object.assign(baseOptions, options.value)
  })

  // ChartData setup
  const compLabels = computed(() => {
    if (chartType === 'time-series')
      return labels.value.map((label) => new Date(label))
    else
      return labels.value
  })
  const chartData = computed(() => {
    let dataSets = datasets.value
    dataSets.forEach((dataset, index) => {
      if (!dataset.borderColor)
        dataset.borderColor = colors[index]
      if (!dataset.backgroundColor)
        dataset.backgroundColor = colors[index]
    })
    let chartData = {
      labels: compLabels.value,
      datasets: dataSets
    }
    return chartData
  })

  return {
    chartData, 
    chartOptions
  }
}