<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed } from 'vue'

import { Line, Bar, Scatter } from 'vue-chartjs'
import { useChartConfig } from './composables'

const props = defineProps({
  chartType: {
    type: String,
    default: 'line',
  },
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
  xTickFormatOptions: {
    type: Object,
    default: {},
  },
  xScaleOptions: {
    type: Object,
    default: null,
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
  yTickFormatOptions: {
    type: Object,
    default: {},
  },
  options: {
    type: Object,
    default: {},
  },
})

const { 
  chartType,
  labels, datasets, title, options,
  xLabel, xTickFormat, xTickPrefix, xTickSuffix, xTickFormatOptions, xScaleOptions,
  yLabel, yTickFormat, yTickPrefix, yTickSuffix , yTickFormatOptions,
  } = toRefs(props)

const { chartData, chartOptions } = useChartConfig({
  chartType,
  labels, datasets, title, options,
  xLabel, xTickFormat, xTickPrefix, xTickSuffix, xTickFormatOptions, xScaleOptions,
  yLabel, yTickFormat, yTickPrefix, yTickSuffix, yTickFormatOptions
})

</script>
  
<template>
  <Line v-if="chartType === 'line'" :data="chartData" :options="chartOptions" />
  <Bar v-else-if="chartType === 'bar'" :data="chartData" :options="chartOptions" />
  <Scatter v-else-if="chartType === 'scatter'" :data="chartData" :options="chartOptions"/>
</template>
  
<style scoped>
  
</style>