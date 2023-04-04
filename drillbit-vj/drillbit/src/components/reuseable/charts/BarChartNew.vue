<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Bar } from 'vue-chartjs'
import { useChartConfig } from './composables'

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
    default: null,
  },
  xTickFormat: {
    type: String,
    default: null,
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
    default: null,
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
  options: {
    type: Object,
    default: null,
  },
  height: {
    type: Number,
    default: 900
  }
})

const { labels, datasets, title, options,
  xLabel, xTickFormat, xTickPrefix, xTickSuffix, 
  yLabel, yTickFormat, yTickPrefix, yTickSuffix 
  } = toRefs(props)

const { chartData, chartOptions } = useChartConfig({ 
  labels, datasets, title, options,
  xLabel, xTickFormat, xTickPrefix, xTickSuffix,
  yLabel, yTickFormat, yTickPrefix, yTickSuffix 
})
</script>
  
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>
  
<style scoped>
  
</style>