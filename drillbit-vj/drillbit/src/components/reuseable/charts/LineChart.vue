<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Line } from 'vue-chartjs'
import vuetify from '@/services/vuetify'
import { useFormatHelpers, hexToRGB } from '../../../services/composables'

const format = useFormatHelpers()

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  legend: {
    type: Object,
    default: {
      display: false,
    },
  },
  title: {
    type: Object,
    default: {
      display: false,
    },
  },
  label: {
    type: String,
    default: null,
  },
  xLabel: {
    type: String,
    required: true,
  },
  xAxisUnit: {
    type: String,
    default: 'quarter',
  },
  xTickPrefix: {
    type: String,
    default: '\u20BF ',
  },
  xTickSuffix: {
    type: String,
    default: '',
  },
  yLabel: {
    type: String,
    required: true,
  },
  height: {
    type: Number,
    default: 900
  },
  yTickFormat: {
    type: String,
    default: null,
  },
  yTickFormatOptions: {
    type: Object,
    default: {},
  },
  yTickPrefix: {
    type: String,
    default: '',
  },
  yTickSuffix: {
    type: String,
    default: '',
  },
})

const { 
  data, xAxisUnit, title, legend, xLabel, 
  yLabel, yTickFormat, yTickPrefix, yTickSuffix, yTickFormatOptions
} = toRefs(props)

const labels = computed(() => {
  let labels = []
  data.value.forEach((object) => {
    labels.push(new Date(object[xLabel.value] + ':00'))}
  )
  return labels
})
const chartData = computed(() => {
  let chartData = {
    labels: labels.value,
    datasets: [{
      label: props.label,
      data: data.value.map((object) => object[yLabel.value]),
    }]
  }
  return chartData
})
const chartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    elements: {
      point: {
        radius: 0
      }
    },
    plugins: {
      title: title.value,
      legend: legend.value
    },
    scales: {
      x: {
        type: 'time',
        time: {
          displayFormats: {
            quarter: 'MMM YYYY'
          }
        },
        time: {
          unit: xAxisUnit.value,
          displayFormats: {
            quarter: 'MMM YYYY',
            year: 'YYYY'
          },
        },
        border: {
          color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
        },
        grid: {
          display: false,
        },
        ticks: {
          callback: (tick) => new Date(tick).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }).split(' '),
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          display: false,
        },
        ticks: { 
          callback: (value, index, ticks) => {
          if (yTickFormat.value) {
            return format[yTickFormat.value](value, yTickFormatOptions.value)
          }
          else
            return yTickPrefix.value + format.number(value) + yTickSuffix.value
        },
        }
      }
    }
  }
})
</script>
  
  
<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
  
<style scoped>
  
</style>