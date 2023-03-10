<script setup>
import { ref, computed, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import MainWindow from '../MainWindow.vue'
import CompWindow from './CompWindow.vue'

import { 
 useEnvironmentStore, 
 useProjectsStore,
 useStatementStore
} from '@/stores/modules'
import { useFormHelpers, TableMaker } from '@/services/composables'

const projectsStore = useProjectsStore()
const envStore = useEnvironmentStore()
const statStore = useStatementStore()
const formHelpers = useFormHelpers()

const { tasksComplete } = storeToRefs(statStore)

const activeIndex = ref(-1)

const runSim = () => {
  /* 
  Run create objects, then execute getSummary and also fetch data for charts afterwards
  */
  let params = []
  projectsStore.object.projects.forEach((project) => {
    params.push({
      environment: envStore.object.id,
      project: project.id,
    })
  })
  return statStore.createObjects({params})
}
watchEffect(() => {
  if (tasksComplete.value) {
    statStore.getByAccount({params: 
      {
        environment: envStore.object.id,
        projects: projectsStore.object.projects.map((project) => project.id)
      }
    })
  }
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
        class="mt-0 pl-3 pr-3"
      />
    <v-combobox
      v-model="projectsStore.object"
      :items="formHelpers.reverse(projectsStore.objects)"
      :rules="formHelpers.nameRules.value"
      item-title="name"
      label="Projects"
      density="compact"
      outlined
      class="mt-0 pl-3 pr-3"
    />
    <div class="d-flex justify-center pt-3">
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
      class="mt-6 pl-3"
    >
      Summary
    </v-list-item>
      <div v-if="projectsStore.object?.projects">
        <v-list-item
          v-for="(project, i) in projectsStore.object.projects"
          @click="activeIndex = i"
          :key="'project' + i"
          :value="i"
          class="pl-3"
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
:deep(.v-btn--variant-outlined) {
  border: 1px solid rgba(var(--v-border-color), .35);
}
</style>