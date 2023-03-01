<script setup>
import { ref, computed } from 'vue'
import { useAsyncState, useAsyncQueue, useStorage } from '@vueuse/core'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import client from '@/services/client'

import { 
  useProjectStore, useProjectsStore, useEnvironmentStore, useSimulationStore, useStatementStore 
} 
  from '@/stores/modules'
const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const envStore = useEnvironmentStore()
const simStore = useSimulationStore()
const statStore = useStatementStore()

const test = ref(null)

const statuses = ref({
  '74a767d9-203f-43b1-89c7-d332490f1d6b': null,
  '068c9104-1f2c-41ff-a360-6e5e54947821': null
})
const tasksComplete = computed(() => {
  return Object.values(statuses.value).every((status) => status === 'SUCCESS')
})

const checkTaskComplete = (task_id, interval, callback) => {
  let intervalId = setInterval(() => {
    client.getProjectTasks({task_id}).then((result) => {
      console.log('before ask', result.data.state)
      if (result.data.state === 'SUCCESS') {
        clearInterval(intervalId)
        callback(result.data)
      } else {
        console.log('not complete', result.data)
      }
    })
  }, interval)
} 
const fetchStatus = () => {
  Object.keys(statuses.value).forEach((task_id) => {
    makePeriodicCallsToURLUntilDone(task_id, 1000, (result) => {
      statuses.value[task_id] = result.state
    })
  })
}
</script>

<template>
  <v-btn
    @click="fetchStatus"
  >Test</v-btn>
  {{ statuses }}
  {{ tasksComplete }}
</template>

  
  
<style scoped>
  
</style>