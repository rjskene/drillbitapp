<script setup>
import 'chartjs-adapter-moment'
import { toRefs, computed, ref, watch, onMounted } from 'vue'

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


// if (chartType.value === 'line') chart.value = line.value
// if (chartType.value === 'bar') chart.value = bar.value
// if (chartType.value === 'scatter') chart.value = scatter.value
// watch(chartType, (newVal, oldVal) => {
//   if (newVal === 'line') chart.value = line.value
//   if (newVal === 'bar') chart.value = bar.value
//   if (newVal === 'scatter') chart.value = scatter.value
// })
const line = ref(null)
const bar = ref(null)
const scatter = ref(null)
const chart = computed(() => {
  if (chartType.value === 'line') return line.value
  if (chartType.value === 'bar') return bar.value
  if (chartType.value === 'scatter') return scatter.value
})
const uri = ref(null)
const chartToImage = () => {
  let uri = chart.value.chart.canvas.toDataURL("image/png", 1)
  let link = document.createElement('a')
  link.download = 'image'
  link.href = uri
  link.click()
}
</script>
  
<template>
  <Line v-if="chartType === 'line'" ref="line" :data="chartData" :options="chartOptions" />
  <Bar v-else-if="chartType === 'bar'" ref="bar" :data="chartData" :options="chartOptions" />
  <Scatter v-else-if="chartType === 'scatter'" ref="scatter" :data="chartData" :options="chartOptions"/>
</template>
  
<style scoped>
  
</style>