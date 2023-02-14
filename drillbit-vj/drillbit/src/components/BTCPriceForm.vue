<script setup>
import { ref, computed, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'

import { useAsyncState } from '@vueuse/core'
import Skeleton from 'primevue/skeleton'

import EnvironmentContainer from './reuseable/EnvironmentContainer.vue'
import Chart from './reuseable/Chart.vue'
import PlaceholderChart from './reuseable/PlaceholderChart.vue'

import { useGlobalStateStore } from '../stores/globalState'
import { useBlockScheduleStore, useBTCPriceStore } from '../stores/modules'
import { useForecastForm, useFormHelpers } from '../services/composables'

const globalState = useGlobalStateStore()
const blockStore = useBlockScheduleStore()
const store = useBTCPriceStore()

const createState = ref(null)
const { object } = storeToRefs(store)
const { nameRules, numberRules, numberIfNotNullRules } = useFormHelpers()

const initial = ref(20000)
const mean = ref(null)
const volatility = ref(null)
const model = ref('Constant')

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
  >>
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
        label="Initial Price"
        class="mt-3 ml-12 py-0"
        prefix="$"
        hide-details
      />
      <v-text-field
        v-model="mean"
        :rules="numberIfNotNullRules"
        label="Mean"
        class="mt-3 ml-12 py-0"
        :disabled="model === 'Constant'"
        hide-details
      />
        <v-text-field
        v-model="volatility"
        :rules="numberIfNotNullRules"
        label="Volatility"
        class="mt-3 ml-12 py-0"
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
      />
    </template>
  </EnvironmentContainer>
</template>

  
<style scoped>
</style>