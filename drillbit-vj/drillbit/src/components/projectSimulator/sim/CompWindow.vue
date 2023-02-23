<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'

import { 
 useProjectStore, useEnvironmentStore, useProjectsStore,
 useSimulationStore, useStatementStore
} from '@/stores/modules'
import { useFormHelpers, TableMaker } from '@/services/composables'

const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const envStore = useEnvironmentStore()
const simStore = useSimulationStore()
const statStore = useStatementStore()
const formHelpers = useFormHelpers()

const columns = computed(() => {
  let cols = [
    {
      field: 'index',
      header: '', 
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-7dot5',
    }
  ]
  projectsStore.object.projects.forEach((project) => {
    cols.push({
      field: project.name,
      header: project.name, 
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-7dot5',
    })
  })

  let table = new TableMaker(cols)
  return table.columns
})
</script>

<template>
  <v-container>
    
  </v-container>
</template>
  
<style scoped>
</style>