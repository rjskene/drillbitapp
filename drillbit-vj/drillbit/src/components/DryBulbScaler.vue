<script setup>
import { computed, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import MainWindow from './projectSimulator/MainWindow.vue'
import BarChart from './reuseable/BarChart.vue'

import { useRejectionStore, useWeatherStationStore, useWeatherDataStore } from '../stores/modules'
import ChartScroll from './reuseable/ChartScroll.vue';

const stationStore = useWeatherStationStore()
const dataStore = useWeatherDataStore()
const rejectionStore = useRejectionStore()

const { objects } = storeToRefs(dataStore)

const view = ref(0)
const region = ref('Texas')
const station = ref('Abilene')
const stationIndex = ref(-1)

const xLabel = 'Dry-Bulb °F'
const yLabel = 'Frequency hr'

stationStore.getRegions()
stationStore.getObjects().then(() => {
  let params = {station: station.value.id}
  dataStore.getObjects(params)
})

const stations = computed(() => {
  if (region.value)
    return stationStore.objects.filter((obj) => obj.region === region.value)
  else
    return []
})
const object = computed(() => {
  return objects.value[0]
})

watch(() => station.value, (newVal, oldVal) => {
  if (newVal) {
    let params = {station: station.value.id}
    dataStore.getObjects(params)
    stationIndex.value = stations.value.findIndex((obj) => obj.id === station.value.id)
  }
})
watch(() => stationIndex.value, (newVal, oldVal) => {
  if (newVal >= 0) {
    station.value = stations.value[newVal]
    let params = {station: station.value.id}
    dataStore.getObjects(params)
  }
})
// () => {
//   if (station.value) {
//     let params = {station: station.value.id}
//     dataStore.getObjects(params)
//     stationIndex.value = stations.value.findIndex((obj) => obj.id === station.value.id)
//   }
// })

</script>

<template>
  <MainWindow>
    <template #nav-panel>
      <v-combobox
        v-model="region"
        :items="stationStore.regions"
        label="Region"
        outlined
        dense
      />
      <v-combobox
        v-model="station"
        :items="stations"
        item-title="location"
        item-value="pk"
        label="Weather Station"
        outlined
        dense
      />
    </template>
    <template #main-panel>
      <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
        <v-toolbar 
          density="compact"
          color="surface"
          class="pt-2"
        >
          <v-btn-toggle
            v-model="view"
            class="mr-6"
            mandatory
          >
            <v-btn>
              Dry Bulb Frequency
            </v-btn>
            <v-btn>
              Profitability Analysis
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
        <ChartScroll
          :num-objects="stations?.length"
          v-model:objects-index="stationIndex"
        >
          <template #chart>
            <BarChart
              v-if="view === 0 && station && object"
              :label="yLabel"
              :xLabel="xLabel"
              :yLabel="yLabel"
              :data="object?.data[yLabel]"
              :labels="object?.data[xLabel]"
            />
          </template>
        </ChartScroll>
      </v-container>
    </template>
  </MainWindow>
    
</template>

<style scoped>
  
</style>

