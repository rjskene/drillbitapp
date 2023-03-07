<script setup>
import { toRefs, computed } from 'vue'

import { Bar } from 'vue-chartjs'
import vuetify from '@/services/vuetify'
import { useFormatHelpers, hexToRGB } from '../../services/composables'

const format = useFormatHelpers()

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  labels: {
    type: Array,
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
    default: '',
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
  }
})
const { data, labels, label, xAxisUnit, title, legend, xLabel, yLabel } = toRefs(props)

const chartData = computed(() => {
  let chartData = {
    labels: labels.value,
    datasets: [{
      label: label.value,
      data: data.value,
    }]
  }
  return chartData
})
const chartOptions = computed(() => {
  return {
    responsive: true,
    // maintainAspectRatio: false,
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
        beginAtZero: true,
        grid: {
          display: false,
        },
        // ticks: { 
        //   callback: (value, index, ticks) => props.xTickPrefix + format.number(value) + props.xTickSuffix,
        // }
      }
    }
  }
})
</script>
  
  
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>
  
<style scoped>
  
</style>