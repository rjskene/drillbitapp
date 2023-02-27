<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Line } from 'vue-chartjs'

import { useFormatHelpers } from '../../services/composables'

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
    default: '',
  },
  height: {
    type: Number,
    default: 900
  }
})

const { labels, datasets, xLabel, yLabel } = toRefs(props)

function formatDateTime(date) {  
    if (!date) return 'NA'
    const options = { year: 'numeric', month: 'short'}
    return date.toLocaleString(undefined, options)
}

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
    labels: labels.value,
    datasets: dataSets
  }
  return chartData
})
const chartOptions = {
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: props.title,
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
        displayFormats: {
          quarter: 'MMM YYYY'
        }
      },
      grid: {
        display: false,
        // borderColor: dark.colors['blue-lighten-4'],
      },
      // ticks: {
      //   callback: (value) => {
      //     console.log(value, formatDateTime(value))
      //     return formatDateTime(value)
      //   },
      // }
    },
    y: {
      beginAtZero: true,
      grid: {
        display: false,
        // borderColor: dark.colors['blue-lighten-4']
      },
      ticks: { 
        // color: dark.colors['blue-lighten-4'],
        callback: (value, index, ticks) => props.xTickPrefix + format.numberWithCommas(value) + props.xTickSuffix,
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