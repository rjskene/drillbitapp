<script setup>
import { ref, computed, toRefs } from 'vue'
import { storeToRefs } from 'pinia'

import PlaceholderChart from '../../reuseable/charts/PlaceholderChart.vue'
import BaseChart from '../../reuseable/charts/BaseChart.vue'

import { useEnvironmentStore } from '@/stores/modules'
import { every_nth } from '../../../services/composables'

const store = useEnvironmentStore()
const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
})
const { loading } = toRefs(props)
const elements = computed(() => {
  return store.elements
})

const allStoresHaveData = computed(() => {
  return elements.value.every((element) => {
    return element.store.object?.data
  })
})

const reshape1dArrayTo2dArray = (array, columns) => {
  const rows = Math.ceil(array.length / columns)
  const newArray = []
  for (let i = 0; i < rows; i++) {
    newArray.push(array.slice(i * columns, i * columns + columns))
  }
  return newArray
}

const updateChartArgs = (element) => {
  let data = element.store.object?.data
  data = every_nth(data, 1000)
  let labels = []
  data.forEach((object) => {
    labels.push(new Date(object['period'] + ':00'))}
  )
  let datasets = [{
    label: element.text,
    data: data.map((object) => {
      let value = object[element.dataKey]
      if (element.text === 'Network Hash Rate') {
        value = value * 10**18 // hack to handle network hash rate b/c number is too big for calculation; see project.serializers line 442 for offsetting hack in backend
      }
      return value
    })
  }]
  return {
    labels,
    datasets,
    title: element.text,
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false},
      }
    },
    xScaleOptions: {
      type: 'time',
      time: {
        unit: 'year',
        displayFormats: {
          quarter: 'YYYY'
        },
      }
    },
    yTickFormat: element.chartOptions.yTickFormat,
    yTickFormatOptions: element.chartOptions.yTickFormatOptions,
  }
}
const chartArgs = computed(() => {
  let chartArgs = {}
  elements.value.forEach((element) => {
    if (element.store.object?.data) {
      chartArgs[element.text] = updateChartArgs(element)
    }
  })
  return chartArgs
})

</script>
  
<template>
  <v-container
    class="h-100"
  >
    <v-row 
      v-if="loading || !allStoresHaveData"
      class="h-100">
      <v-col class="d-flex align-center justify-center h-100">
        <v-progress-circular
            v-if="loading"
            indeterminate
            color="secondary"
          />
          <PlaceholderChart 
            v-else
          />
      </v-col>
    </v-row>
    <v-row
      v-else
      v-for="row in reshape1dArrayTo2dArray(elements, 2)"
      class="d-flex justify-space-around"
    >
      <v-col
        v-for="element in row" :key="element.text"
        cols="6"
      >
        <div 
          style="min-height: 300px"
          class="d-flex justify-center align-center"
        >
          <BaseChart
            v-bind="chartArgs[element.text]"
          />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  
<style scoped>
  
</style>