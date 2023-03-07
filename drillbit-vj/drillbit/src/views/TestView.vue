<script setup>
import { ref, computed } from 'vue'
import { useAsyncState, useAsyncQueue, useStorage } from '@vueuse/core'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import ScatterPlusLineChart from '@/components/reuseable/ScatterPlusLineChart.vue'

import client from '@/services/client'

import { 
  useProjectStore, useProjectsStore, useEnvironmentStore, useSimulationStore, useStatementStore,
  useCurveStore,
} 
  from '@/stores/modules'
const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const envStore = useEnvironmentStore()
const simStore = useSimulationStore()
const statStore = useStatementStore()

const curveStore = useCurveStore()

const xLabel = 'Ambient Temp (F)'
const yLabel = 'Capacity (W)'
const generateLine = (slope, intercept) => {
  return (xValues) => {
    return xValues.map((x) => {
      console.log(x)
      return slope * x + intercept
    })
  }
}
const xValues = computed(() => {
  return curveStore.object ? curveStore.object.curve.raw[xLabel] : []
})
const lineYValues = computed(() => {
  return curveStore.object ? generateLine(curveStore.object.curve.a, curveStore.object.curve.b)(xValues.value) : []
})
const scatterValues = computed(() => {
  let result = []
  if (curveStore.object) {
    let obj = curveStore.object.curve.raw
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
<v-btn
  @click="curveStore.getObject({pk: 2})"
></v-btn>

{{ curveStore.object }}
{{ xValues  }}

<ScatterPlusLineChart
  v-if="curveStore.object"
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