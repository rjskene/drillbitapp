<script setup>
import { ref, computed } from 'vue'
import { useAsyncState, useAsyncQueue, useStorage } from '@vueuse/core'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'

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

const state = useStorage('test', test)
</script>

<template>
  <v-text-field
  v-model="test"
  label="Test"
  outlined
  dense
  class="mt-0"
  />
  {{ test }}
</template>
  
  
<style scoped>
  
</style>