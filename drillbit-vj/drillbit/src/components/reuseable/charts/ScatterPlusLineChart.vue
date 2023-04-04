<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Scatter } from 'vue-chartjs'
import vuetify from '@/services/vuetify'
import { useFormatHelpers, hexToRGB } from '../../../services/composables'

const format = useFormatHelpers()

const props = defineProps({
  labels: {
    type: Array,
    required: true,
  },
  lineLabel: {
    type: String,
    default: '',
  },
  scatterLabel: {
    type: String,
    default: '',
  },
  lineYValues: {
    type: Array,
    required: true,
  },
  scatterValues: {
    type: Array,
    required: true,
  },
  title: {
    type: String,
    default: '',
  },
  xLabel: {
    type: String,
    default: '',
  },
  yTickFormat: {
    type: String,
    default: null,
  },
  yTickPrefix: {
    type: String,
    default: '',
  },
  yTickSuffix: {
    type: String,
    default: '',
  },
  yLabel: {
    type: String,
    default: '',
  },
  height: {
    type: Number,
    default: 900
  }
})

const { 
  labels, lineLabel, scatterLabel, 
  lineYValues, scatterValues, title, 
  yTickFormat, xLabel, yLabel, yTickPrefix, yTickSuffix 
} = toRefs(props)

const colors = [
  '#3a5ba9', // primary variant 1
  '#80ba56', // secondary
  '#6b88cc', // primary variant 1 lighten 30%
  '#adbde3', // primary variant 1 lighten 60%
  '#cde4bd', // secondary lighten 30%
  '#a6cf89', // secondary lighten 60%
]
const chartData = computed(() => {
  let datasets = [
    {
      type: 'line',
      label: lineLabel.value,
      data: lineYValues.value,
      backgroundColor: colors[0],
      borderColor: colors[0],
      xAxisID: 'x2', // Specify to which axes to link
      elements: {
        point: {
          radius: 0
        }
      },
    },
    {
      type: 'scatter',
      label: scatterLabel.value,
      backgroundColor: colors[1],
      borderColor: colors[1],
      data: scatterValues.value
    }
  ]
  let chartData = {
    labels: labels.value.map((label) => new Date(label)),
    datasets
  }
  return chartData
})
const chartOptions = {
  responsive: true,
  aspectRatio: 1.5,
  plugins: {
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
  },
  scales: {
    x: {
      title: {
        display:true, 
        text: xLabel.value,
      },
      border: {
        color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
      },
      grid: {
        display: false,
      },
      // ticks: {
      //   callback: (tick) => new Date(tick).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }).split(' '),
      // },
    },
    x2: {
      display: false,
      border: {
        color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
      },
      grid: {
        display: false,
      },
      // ticks: {
      //   callback: (tick) => new Date(tick).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }).split(' '),
      // },
       
    },
    y: {
      title: {
        display:true, 
        text: yLabel.value,
      },
      border: {
        color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
      },
      grid: {
        display: false,
      },
      ticks: { 
        callback: (value, index, ticks) => {
          if (yTickFormat.value) {
            return format[yTickFormat.value](value)
          }
          else
            return yTickPrefix.value + format.number(value) + yTickSuffix.value
        },
      }
    }
  }
}
</script>
  
  
<template>
  <Scatter :data="chartData" :options="chartOptions" />
</template>
  
<style scoped>
  
</style>