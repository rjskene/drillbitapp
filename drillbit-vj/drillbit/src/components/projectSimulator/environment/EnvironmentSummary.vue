<script setup>
import { ref, computed } from 'vue'

import PlaceholderChart from '../../reuseable/PlaceholderChart.vue'
import Chart from '../../reuseable/Chart.vue'

import { useEnvironmentStore } from '@/stores/modules'
import { every_nth } from '../../../services/composables'

const store = useEnvironmentStore()

const props = defineProps({
  elements: {
    type: Array,
    required: true,
  },
})

const reshape1dArrayTo2dArray = (array, columns) => {
  const rows = Math.ceil(array.length / columns)
  const newArray = []
  for (let i = 0; i < rows; i++) {
    newArray.push(array.slice(i * columns, i * columns + columns))
  }
  return newArray
}
</script>
  
  
<template>
  <!-- !createState?.isLoading &&  -->
  <v-row 
    v-for="(row, i) in reshape1dArrayTo2dArray(elements, 2)" 
    :key="'row-' + i"
    class="d-flex justify-space-evenly h-100 my-3"
  >
    <v-col 
      v-for="element in row" :key="element.text"
      class="ma-0 ml-1 pa-0"
    >
      <PlaceholderChart v-if="!element.store.object?.data"></PlaceholderChart>
      <Chart 
        v-else-if="element.store.object?.data"
        :data="every_nth(element.store.object.data, 1000)"
        :label="element.text"
        x-label="period"
        :x-tick-prefix="element.xTickPrefix"
        :x-tick-suffix="element.xTickSuffix"
        :y-label="element.yLabel"
      />
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>