<script setup>
import { ref, computed, toRefs } from 'vue'

import ScatterPlusLineChart from '@/components/reuseable/charts/ScatterPlusLineChart.vue'

const props = defineProps({
  object: {
    type: Object,
    required: true,
  },
})
const { object } = toRefs(props)
const xLabel = 'Ambient Temp (F)'
const yLabel = 'Capacity (W)'
const generateLine = (slope, intercept) => {
  return (xValues) => {
    return xValues.map((x) => {
      return slope * x + intercept
    })
  }
}
const xValues = computed(() => {
  return object ? object.value.curve.raw[xLabel] : []
})
const lineYValues = computed(() => {
  return object ? generateLine(object.value.curve.a, object.value.curve.b)(xValues.value) : []
})
const scatterValues = computed(() => {
  let result = []
  if (object) {
    let obj = object.value.curve.raw
    for (let i = 0; i < obj[xLabel].length; i++) {
      result.push({
        x: obj[xLabel][i],
        y: obj[yLabel][i],
      })
    }
  }
  return result
})

</script>

<template>
  <ScatterPlusLineChart
    v-if="object"
    lineLabel="Regression"
    scatterLabel="Data"
    :labels="xValues"
    :lineYValues="lineYValues"
    :scatterValues="scatterValues"
    yTickFormat="power"
    :xLabel="xLabel"
    :yLabel="yLabel.split(' ')[0]"
  />
</template>

  
  
<style scoped>
  
</style>