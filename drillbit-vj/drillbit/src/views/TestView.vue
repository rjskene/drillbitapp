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

const checkForStatements = async () => {
  const res = await client.checkStatementExists({
    params: {
      environment: envStore.object.id,
      projects: [61, 65, 999]
    }
  })
  test.value = res.data
}

</script>

<template>
  <v-btn
    @click="checkForStatements"
  >Test</v-btn>
  {{ test }}
</template>

  
  
<style scoped>
  
</style>