<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import MainWindow from '../MainWindow.vue'
import CompWindow from './CompWindow.vue'

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

const activeIndex = ref(0)

const runSim = () => {
  let params = []
  projectsStore.object.projects.forEach((project) => {
    params.push({
      environment: envStore.object.id,
      project: project.id,
      frequency: 'M'
    })
  })
  return statStore.createObjects({params}).then(() => {
    statStore.getSummary({
      params: { 
        environment: envStore.object.id,
        projects: projectsStore.object.projects.map((project) => project.id)
      }
    })
  })
}
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
  <MainWindow>
    <template #nav-panel>
      <v-combobox
        v-model="envStore.object"
        :items="formHelpers.reverse(envStore.objects)"
        :rules="formHelpers.nameRules.value"
        item-title="name"
        label="Environment"
        density="compact"
        outlined
        class="mt-0"
      />
    <v-combobox
      v-model="projectsStore.object"
      :items="formHelpers.reverse(projectsStore.objects)"
      :rules="formHelpers.nameRules.value"
      item-title="name"
      label="Projects"
      density="compact"
      outlined
      class="mt-0"
    />
    <div class="d-flex justify-center">
      <StatefulBtn
        @click="runSim"
        variant="outlined"
        label="Run"
        icon="mdi-play"
        size="large"
      />
    </div>
    <v-card-subtitle class="mt-8"></v-card-subtitle>
    <v-divider></v-divider>
    <v-list-item
      @click="activeIndex = -1"
      key="summary"
      value="4"
      class="mt-6"
    >
      Summary
    </v-list-item>
      <div v-if="projectsStore.object?.projects">
        <v-list-item
          v-for="(project, i) in projectsStore.object.projects"
          @click="activeIndex = i"
          :key="'project' + i"
          :value="i"
        >
          {{ project.name }}
        </v-list-item>
      </div>
    </template>
    <template #main-panel>
      <div 
        v-if="activeIndex === -1"
        class="d-flex justify-center"
      >
        <CompWindow></CompWindow>
      </div>
    </template>
  </MainWindow>
</template>
  
<style scoped>
:deep(.v-combobox > .v-input__append) {
  padding: 0;
}
</style>