<script setup>
import { ref, watchEffect, computed } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import MainWindow from '../MainWindow.vue'
import CompWindow from './CompWindow.vue'

import { createPPTX } from '../../../services/ppt'

import { 
 useEnvironmentStore, 
 useProjectsStore,
 useSimulationStore,
 useStatementStore
} from '@/stores/modules'
import { useFormHelpers } from '@/services/composables'
import ProjectFinancialStatements from './ProjectFinancialStatements.vue'

const projectsStore = useProjectsStore()
const envStore = useEnvironmentStore()
const simStore = useSimulationStore()
const statStore = useStatementStore()
const formHelpers = useFormHelpers()

const { nTasksToComplete, nTasksComplete, hasTasks, projectTasksComplete} = storeToRefs(statStore)
const taskProgress = computed(() => {
  return 100 * nTasksComplete.value / nTasksToComplete.value
})

const overwrite = ref(false)
const activeIndex = ref(-1)

// Watch environment and projects
// If either one changes, and there is values for both
// get_or_create sims objects for each combination and store them
// in the simStore
// for createObjects, need to send list of combined environment and project elements
watchEffect(() => {
  if (envStore.object && projectsStore.object?.projects?.length > 0) {
    let params = simStore.simsByAttrs
    simStore.createObjects({params})
  }
})

const runSim = () => {
  /* 
  Run create objects, then execute getSummary and also fetch data for charts afterwards
  */
  let params = simStore.objects.map((sim) => sim.id)
  return statStore.createObjects({params, overwrite: overwrite.value})
    .then(() => {
      overwrite.value = false
      // must use django rest filtering syntax
      // https://stackoverflow.com/questions/31029792/how-do-you-use-the-django-filter-package-with-a-list-of-parameters
      let sims = simStore.objects.map((sim) => sim.id).join(',')
      statStore.getObjects({sim__in: sims, frequency: 'M'})
    })
}
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
    <v-checkbox 
      v-model="overwrite"
      label="Overwrite existing"
      class="mt-6"
    />
    <v-btn
      @click="createPPTX"
      icon="mdi-file-powerpoint-box-outline"
    ></v-btn>
    <div class="d-flex justify-center pt-3">
      <StatefulBtn
        @click="runSim"
        :disabled="!simStore.objects || simStore.objects.length === 0"
        variant="outlined"
        label="Run"
        icon="mdi-play"
        size="large"
      />
    </div>
    <v-card-subtitle class="mt-8"></v-card-subtitle>
    <v-progress-linear
      v-if="hasTasks"
      v-model="taskProgress"
      :stream="taskProgress < 100"
    />
    <v-divider></v-divider>
    <v-list-item
      @click="activeIndex = -1"
      key="summary"
      :value="-1"
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
        :disabled="(simStore.objects.find(obj => obj.project === project.id) === undefined) && (Object.keys(projectTasksComplete).includes(project.id) && !projectTasksComplete[project.id])"
        class="pl-3"
      >
        {{ project.name }}
      </v-list-item>
    </div>
    </template>
    <template #main-panel>
      <v-container>
        <v-row class="h-100">
          <v-col class="h-100">
            <CompWindow v-if="activeIndex === -1"/>
            <ProjectFinancialStatements
              v-else
              :sim="simStore.objects[activeIndex]"
            >
            </ProjectFinancialStatements>
          </v-col>
        </v-row>
      </v-container>
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