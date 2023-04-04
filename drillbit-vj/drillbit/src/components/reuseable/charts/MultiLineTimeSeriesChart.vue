<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Line } from 'vue-chartjs'
import vuetify from '@/services/vuetify'
import { useFormatHelpers, hexToRGB } from '../../services/composables'

const format = useFormatHelpers()

const props = defineProps({
  labels: {
    type: Array,
    required: true,
  },
  datasets: {
    type: Object,
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

const { labels, datasets, title, yTickFormat, xLabel, yLabel, yTickPrefix, yTickSuffix } = toRefs(props)

const colors = [
  '#3a5ba9', // primary variant 1
  '#80ba56', // secondary
  '#6b88cc', // primary variant 1 lighten 30%
  '#adbde3', // primary variant 1 lighten 60%
  '#cde4bd', // secondary lighten 30%
  '#a6cf89', // secondary lighten 60%
]
const chartData = computed(() => {
  let dataSets = datasets.value
  dataSets.forEach((dataset, index) => {
    dataset.borderColor = colors[index]
    dataset.backgroundColor = colors[index]
  })
  let chartData = {
    labels: labels.value.map((label) => new Date(label)),
    datasets: dataSets
  }
  return chartData
})
const chartOptions = {
  responsive: true,
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
  elements: {
    point: {
      radius: 0
    }
  },
  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'quarter',
        displayFormats: {
          quarter: 'MMM YYYY'
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
            return yTickPrefix.value + format.numberWithCommas(value) + yTickSuffix.value
        },
      }
    }
  }
}
</script>
  
  
<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
  
<style scoped>
  
</style>