<script setup>
import { ref, computed, defineExpose, watch, watchEffect} from 'vue'
import { storeToRefs } from 'pinia'
import Skeleton from 'primevue/skeleton'

import EnvironmentContainer from './reuseable/EnvironmentContainer.vue'
import Chart from './reuseable/Chart.vue'
import PlaceholderChart from './reuseable/PlaceholderChart.vue'

import { getTodayAsString, useFormHelpers, useEnviroForm } from '../services/composables'
import { useBlockScheduleStore } from '../stores/modules'

const {nameRules, startDateRules, endDateRules} = useFormHelpers()
const store = useBlockScheduleStore()

const startDate = ref(getTodayAsString())
const endDate = ref(5)
const createState = ref(null)
const { object } = storeToRefs(store)

const btnProps = {
  elevation: 0,
  size: 'x-small',
  class: 'mx-0',
}
const createParams = computed (() => {
  return {start_date: startDate.value, last_epoch: endDate.value}
})
const enviroForm = useEnviroForm({createFunc: store.createObjects, createState, params: createParams})

</script>
  
<template>
  <EnvironmentContainer 
    :name="store.$id.replace('Store', '')"
    :on-save="enviroForm.getOrCreate"
  >
    <template #fields>
      <v-text-field
        v-model="startDate"
        :rules="startDateRules"
        label="Start"
        clearable
        hide-details
        class="mt-1 mr-12"
      />
      <v-text-field
        v-model="endDate"
        :rules="endDateRules"
        label="End"
        clearable
        hint="Date or Epoch"
        class="mt-6 ml-12"
      />
    </template> 
    <template #chart>
      <Skeleton v-if="createState?.isLoading" width="100%" height="500px"></Skeleton>
      <PlaceholderChart v-else-if="!createState?.isLoading && !store.object?.data"></PlaceholderChart>
      <Chart 
        v-else-if="store.object?.data"
        :data="enviroForm.every_nth(store.object.data, 1000)"
        x-label="period"
        y-label="reward"
      />
    </template>
  </EnvironmentContainer>
  

</template>
  
<style scoped>
::v-deep(.p-skeleton) {
  background-color: rgb(var(--v-theme-surface));
}
</style>