<script setup>
import { ref, computed, toRefs, defineExpose } from 'vue'

import Chart from '../../reuseable/Chart.vue'
import PlaceholderChart from '../../reuseable/PlaceholderChart.vue'
import Skeleton from 'primevue/skeleton'

import { every_nth } from '../../../services/composables'

const props = defineProps({
  createState: {
    type: Object,
    required: true,
    default: null,
  },
  activeElement: {
    type: Object,
    required: true
  }
})
const { createState, activeElement } = toRefs(props)
const activeStore = computed(() => {
  return activeElement.value.store
})

const form = ref(null)
const valid = computed(() => {
  return form.value.errors.length === 0
})
defineExpose({
  valid
})
</script>
  
  
<template>
  <v-row>
    <v-col class="mt-12 mx-6">
      <v-form ref="form">
        <v-sheet class="d-flex justify-space-evenly">
          <v-sheet
            v-for="field in activeStore.formFields"
            :key="field.name"
            class="w-25 mx-6"
          >
            <v-select
              v-if="field.type && field.type === 'select'"
              v-model="activeStore.formParams[field.name]"
              v-bind="field"
              density="compact"
            />
            <v-text-field
              v-else
              v-model="activeStore.formParams[field.name]"
              v-bind="field"
              density="compact"
            />
          </v-sheet>
        </v-sheet>
      </v-form>
    </v-col>
  </v-row>
  <v-row>
    <v-col class="mt-12 mx-6">
      <Skeleton v-if="createState?.isLoading" width="95%" height="500px"></Skeleton>
      <PlaceholderChart v-else-if="!createState?.isLoading && !activeStore.object?.data"></PlaceholderChart>
      <Chart 
        v-else-if="activeStore.object?.data"
        :data="every_nth(activeStore.object.data, 1000)"
        :label="activeElement.text"
        x-label="period"
        :y-label="activeElement.yLabel"
        :x-tick-prefix="activeElement.xTickPrefix"
        :x-tick-suffix="activeElement.xTickSuffix"
      />
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>