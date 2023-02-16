<script setup>
import { ref, computed } from 'vue'

import Skeleton from 'primevue/skeleton'
import { useAsyncState } from '@vueuse/core'

import EnvironmentContainer from './reuseable/EnvironmentContainer.vue'
import Chart from './reuseable/Chart.vue'
import PlaceholderChart from './reuseable/PlaceholderChart.vue'

import { useGlobalStateStore } from '../stores/globalState'
import { useBlockScheduleStore, useHashRateStore } from '../stores/modules'
import { useForecastForm, useFormHelpers } from '../services/composables'

const globalState = useGlobalStateStore()
const store = useHashRateStore()
const blockStore = useBlockScheduleStore()

const { nameRules, numberRules, numberIfNotNullRules } = useFormHelpers()

const initial = ref(225)
const mean = ref(null)
const volatility = ref(null)
const model = ref('Constant')
const createState = ref(null)

const forecast = computed(() => {
  return useForecastForm({
    blocks: blockStore.object?.id,
    initial,
    mean, 
    volatility,
    model,
    createFunc: store.createObjects,
    createState,
  })}
)
</script>
  
<template>
  <EnvironmentContainer 
    :name="store.$id.replace('Store', '')"
    :on-save="forecast.enviroForm.getOrCreate"
  >
    <template #fields>
      <v-select
        v-model="model"
        :items="forecast.models"
        label="Model"
        class="mt-3 px-12 py-0"
        hide-details
      />
      <v-text-field
        v-model="initial"
        :rules="numberRules"
        label="Initial Rate"
        class="mt-3 px-12 py-0"        
        suffix="M TH/s"
        hide-details
        />
      <v-text-field
        v-model="mean"
        :rules="numberIfNotNullRules"
        label="Mean"
        class="mt-3 px-12 py-0"
        :disabled="model === 'Constant'"
        hide-details
        />
        <v-text-field
        v-model="volatility"
        :rules="numberIfNotNullRules"
        label="Volatility"
        class="mt-3 px-12 py-0"
        :disabled="model === 'Constant' || model === 'CGR'"
        hide-details
      />
    </template>
    <template #chart>
      <Skeleton v-if="createState?.isLoading" width="100%" height="500px"></Skeleton>
      <PlaceholderChart v-else-if="!createState?.isLoading && !store.object?.data"></PlaceholderChart>
      <Chart 
        v-else-if="store.object?.data"
        :data="forecast.enviroForm.every_nth(store.object.data, 1000)"
        x-label="period"
        y-label="forecast"
        x-tick-prefix=""
        x-tick-suffix="M TH/s"
      />
    </template>
  </EnvironmentContainer>
</template>
  
  
<style scoped>
</style>