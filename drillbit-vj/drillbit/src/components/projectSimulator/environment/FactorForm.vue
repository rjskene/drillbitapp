<script setup>
import { ref, computed, toRefs, defineExpose, watch, onMounted } from 'vue'

import BaseChart from '../../reuseable/charts/BaseChart.vue'
import PlaceholderChart from '../../reuseable/charts/PlaceholderChart.vue'

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

// Form Details
const form = ref(null)
const valid = computed(() => {
  return form.value.errors.length === 0
})

defineExpose({
  valid
})

// Chart Data and Formatting
const { createState, activeElement } = toRefs(props)
const activeStore = computed(() => {
  return activeElement.value.store
})
const data = computed(() => {
  return activeStore.value.object?.data
})
const chartArgs = ref(null)
const updateChartArgs = (data) => {
  data = every_nth(data, 1000)
  let labels = []
  data.forEach((object) => {
    labels.push(new Date(object['period'] + ':00'))}
  )
  
  let datasets = [{
    label: activeElement.value?.text,
    data: data.map((object) => {
      let value = object[activeElement.value?.dataKey]
      if (activeElement.value?.text === 'Network Hash Rate') {
        value = value * 10**18 // hack to handle network hash rate b/c number is too big for calculation; see project.serializers line 442 for offsetting hack in backend
      }
      return value
    })
  }]
  chartArgs.value = {
    labels,
    datasets,
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },    
      },
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
    yTickFormat: activeElement.value?.chartOptions.yTickFormat,
    yTickFormatOptions: activeElement.value?.chartOptions.yTickFormatOptions,
  }
}
watch(data, (data) => {
  if (data)
    updateChartArgs(data)
})
</script>
  
<template>
  <v-row>
    <v-col class="mx-6 mt-3">
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
    <v-col class="mb-3 mx-6">
      <div 
        style="min-height: 550px"
        class="d-flex justify-center align-center"
      >
        <v-progress-circular
          v-if="createState?.isLoading"
          indeterminate
          color="secondary"
        />
        <PlaceholderChart v-else-if="!createState?.isLoading && !activeStore.object?.data"></PlaceholderChart>
        <BaseChart
          v-else-if="chartArgs"
          ref="chart"
          v-bind="chartArgs"
        />
      </div>
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>