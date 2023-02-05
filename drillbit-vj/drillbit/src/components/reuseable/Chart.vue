<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Line } from 'vue-chartjs'

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  xLabel: {
    type: String,
    required: true,
  },
  yLabel: {
    type: String,
    required: true,
  },
  height: {
    type: Number,
    default: 300
  }
})

const { data, xLabel, yLabel } = toRefs(props)

const labels = computed(() => {
  let labels = []
  data.value.forEach((object) => {
    labels.push(new Date(object[xLabel.value] + ':00'))}
  )
  return labels
})
function formatDateTime(date) {
  
      if (!date) return 'NA'
      const options = { year: 'numeric', month: 'short'}
      return date.toLocaleString(undefined, options)
}
const chartData = computed(() => {
  let chartData = {
    labels: labels.value,
    datasets: [{
      label: 'Block Reward',
      data: data.value.map((object) => object[yLabel.value]),
      // backgroundColor: vuetify.theme.themes.value.light.colors.green,
    }]
  }
  return chartData
})
const chartOptions = {
  responsive: true,
  // maintainAspectRatio: false,
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
        callback: (value, index, ticks) => '\u20BF ' + value,
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