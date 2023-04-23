<script setup>
import { storeToRefs } from 'pinia'
import { ref, computed, watch, watchEffect, onMounted } from 'vue'

import { useAsyncState } from '@vueuse/core'

import MainWindow from '../components/projectSimulator/MainWindow.vue'
import ChartScroll from '../components/reuseable/charts/ChartScroll.vue'
import BaseChart from '../components/reuseable/charts/BaseChart.vue'

import { 
  useWeatherStationStore, 
  useWeatherDataStore,
} from '../stores/modules'

const stationStore = useWeatherStationStore()
const dataStore = useWeatherDataStore()

const region = ref('Texas') // Regions are only brought over as the name, not objects; so no need to search thru index
const station = ref(null)
const stationIndex = ref(-1)
const variable = ref('Dry-Bulb')
const type = ref('Single-Variable Frequency')
const period = ref('Annual')

const { objects, types: baseTypes, variables, periods: basePeriods } = storeToRefs(dataStore)

const loadState = ref(null)
const stations = computed(() => {
  if (region.value)
    return stationStore.objects.filter((obj) => obj.region === region.value)
  else
    return []
})
const types = computed(() => {
  let types = baseTypes.value
  types.push('Simulation')
  return types 
})
const periods = computed(() => {
  var periods
  if (type.value === 'Simulation')
    periods = ['Annual']
  else
    periods = basePeriods.value
  return periods
})
const getObjectsParams = computed(() => {
  return {
    station: station.value.id,
    variable: variable.value,
    type: type.value,
    period: period.value,
  }
})
const object = computed(() => {
  return objects.value[0]
})

watch(() => stations.value, (newVal, oldVal) => {
  if (newVal.length > 0) {
    station.value = stations.value[0]
  }
})
watch(() => station.value, (newVal, oldVal) => {
  if (newVal) {
    stationIndex.value = stations.value.findIndex((obj) => obj.id === station.value.id)
  }
})
watch(() => stationIndex.value, (newVal, oldVal) => {
  if (newVal >= 0) {
    station.value = stations.value[newVal]
  }
})
watch(() => type.value, (newVal, oldVal) => {
  if (newVal === 'Simulation')
      period.value = 'Annual'
      variable.value = 'Dry-Bulb'
  if (newVal === 'Diurnal' && oldVal !== 'Diurnal')
      period.value = 'Jan'
  if (type.value === 'Single-Variable Frequency' && oldVal !== 'Single-Variable Frequency')
      period.value = 'Annual'
})
watchEffect(() => {
  if (station.value && variable.value && type.value && period.value) {
    dataStore.getTypes({})
    dataStore.getVariables({type: type.value})
    dataStore.getPeriods({type: type.value, variable: variable.value})
    console.log(getObjectsParams.value)
    loadState.value = useAsyncState(
      dataStore.getObjects(getObjectsParams.value).then(() => {
        console.log(dataStore.objects)
        updateChartArgs()
      })
    )
  }
})
onMounted(() => {
  stationStore.getObjects().then(() => {
    let initIndex = stationStore.objects.findIndex((obj) => obj.location === 'Abilene')    
    station.value = stationStore.objects[initIndex]
    loadState.value = useAsyncState(dataStore.getObjects(getObjectsParams.value).then(() => updateChartArgs()))
  })
})

// Chart Configs
const chartArgs = ref(null)
const updateChartArgs = () => {
  var labels = []
  var datasets = []
  if (object.value && type.value === 'Diurnal') {
    labels = object.value?.data["Hour"]
    Object.entries(object.value?.data).forEach(([key, value]) => {
      if (key !== "Hour" && key !== "Average °F") {
        datasets.push({
          type: 'line',
          label: key,
          data: value,
          order: value - 1
        })
      }
    })
    chartArgs.value = {chartType: 'line', labels, datasets}
  } else if (object.value && type.value === 'Single-Variable Frequency' && variable.value === 'Dry-Bulb') {
    labels = object.value?.data["Dry-Bulb °F"]
    datasets.push({
      label: 'Frequency hr',
      data: object.value?.data['Frequency hr'],
    })
    chartArgs.value = {
      chartType: 'bar',
      labels, datasets, xLabel: 'Dry-Bulb °F', yLabel: 'Frequency hr',
      options: {plugins: {legend: {display: false}}}
    }
  } else if (object.value && type.value === 'Simulation') {
    labels = object.value?.periods
    datasets.push({
      label: 'Dry-Bulb °F',
      data: object.value?.data,
    })
    chartArgs.value = {
      chartType: 'scatter', 
      labels, 
      datasets,
      xScaleOptions: {
        type: 'time',
        time: {
          unit: 'quarter',
          displayFormats: {
            quarter: 'MMM YYYY'
          },
        }
      }
    }
  }
}
</script>
  
<template>
  <v-card 
    class="mx-10 my-5 pa-0 rounded-xl"
    min-height="1200px"
    color="background"
  >
    <v-card-title>Station Data</v-card-title>
    <MainWindow>
      <template #nav-panel>
        <v-combobox
          v-model="region"
          :items="stationStore.regions"
          label="Region"
          outlined
          dense
          class="mt-0 pl-3 pr-3"
        />
        <v-combobox
          v-model="station"
          :items="stations"
          item-title="location"
          item-value="id"
          label="Weather Station"
          outlined
          dense
          class="mt-0 pl-3 pr-3"
        />
        <v-combobox
          v-model="type"
          :items="types"
          label="Data Type"
          outlined
          dense
          class="mt-0 pl-3 pr-3"
        />
        <v-combobox
          v-model="variable"
          :items="variables"
          label="Data Variable"
          outlined
          dense
          class="mt-0 pl-3 pr-3"
        />
        <v-combobox
          v-model="period"
          :items="periods"
          :disabled="!periods[0] || type === 'Simulation'"
          label="Period"
          outlined
          dense
          class="mt-0 pl-3 pr-3"
        />
      </template>
      <template #main-panel>
        <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
          <v-toolbar 
            density="compact"
            color="surface"
            class="pt-2"
          >
          </v-toolbar>
          <v-card
            v-if="!loadState || loadState.isLoading"
            elevation="0"
            class="d-flex justify-center align-center"
            min-height="535px"
          >
            <v-sheet>
              <v-progress-circular
                color="secondary"
                indeterminate
              ></v-progress-circular>
            </v-sheet>
          </v-card>
          <ChartScroll
            v-else
            :num-objects="stations?.length"
            v-model:objects-index="stationIndex"
          >
            <template #chart>
              <BaseChart
                v-if="chartArgs"
                v-bind="chartArgs"
              />
            </template>
          </ChartScroll>
        </v-container>
      </template>
    </MainWindow>    
  </v-card>
</template>

  
<style scoped>
:deep(.tab-color-surface) {
  background-color: rgb(var(--v-theme-surface));

}
</style>