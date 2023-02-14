<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from './reuseable/StatefulBtn.vue'
import ProjectForm from './ProjectForm.vue'
import BlockScheduleForm from './BlockScheduleForm.vue'
import BTCPriceForm from './BTCPriceForm.vue'
import TransactionFeesForm from './TransactionFeesForm.vue'
import NetworkHashRateForm from './NetworkHashRateForm.vue'

import { 
  useBlockScheduleStore, useBTCPriceStore, useFeeStore, useHashRateStore,
  useProjectStore, useEnvironmentStore, useProjectsStore,
} from '../stores/modules'
import { useFormHelpers } from '../services/composables'

const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const environmentStore = useEnvironmentStore()
const formHelpers = useFormHelpers()

const { projects } = storeToRefs(projectStore)
const { environment } = storeToRefs(environmentStore)

const activeElement = ref(0)
const activeProject = computed(() => {
  return activeElement.value - 5
})

const enviroElements = [
  {text: 'Block Schedule', value: 0, form: BlockScheduleForm, store: useBlockScheduleStore()},
  {text: 'BTC Price', value: 1, form: BTCPriceForm, store: useBTCPriceStore()},
  {text: 'Transaction Fees', value: 2, form: TransactionFeesForm, store: useFeeStore()},
  {text: 'Network Hash Rate', value: 3, form: NetworkHashRateForm, store: useHashRateStore()}
]

const readyOrNot = (item) => {
  if (item.store) {
    return {
      icon: environmentStore.locked[item.store.$id.replace('Store', '')] ? 'mdi-check' : 'mdi-close',
      color: environmentStore.locked[item.store.$id.replace('Store', '')] ? 'secondary' : 'error'
    }
  }
  return {}
}
const loadEnvironment = (params) => {
  if (typeof params === 'string' || params instanceof String)
    environmentStore.$patch((state) => {
      state.environment.name = params
    })
  else
    environmentStore.load(params)
}
const loadProjects = (params) => {
  if ((typeof params === 'string' || params instanceof String))
    projectsStore.$patch((state) => {
      state.object = {name: params}
    })
  else if (params)
    projectsStore.load(params)
}
const copyProject = (project) => {
  const {['id']: _, ...params} = project
  projectStore.create(params)
}

const removeKeyFromObject = (obj, key) => {

}
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <v-list
          nav
          density="compact"
        >
          <v-list-subheader class="text-subtitle-1">Environment</v-list-subheader>
          <v-combobox
            @update:modelValue="(params) => loadEnvironment(params)"
            :items="environmentStore.objects"
            item-title="name"
            density="compact"
            outlined
            clearable
            class="mt-0"
          >
          <template #append>
            <StatefulBtn
              @click="environmentStore.save"
              variant="flat"
              icon="mdi-content-save"
              size="small"
              :disabled="!environmentStore.allLocked"
            />
            </template>
          </v-combobox>
          <v-list-item
            v-for="item in enviroElements"
            @click="activeElement = item.value"
            :key="item.text + '-enviroElement'"
            :value="item.value"
          >
            {{ item.text }}
            <template #append>
              <v-icon v-bind="readyOrNot(item)"></v-icon>
            </template>
          </v-list-item>
          <!-- use subheader as spacer -->
          <v-list-subheader></v-list-subheader>
          <v-divider/>
          <!-- use subheader as spacer -->
          <v-list-subheader class="mt-1"></v-list-subheader>
          <v-list-subheader class="text-subtitle-1">Projects</v-list-subheader>
          <v-combobox
            @update:modelValue="(params) => loadProjects(params)"
            :items="projectsStore.objects"
            item-title="name"
            density="compact"
            outlined
            clearable
            class="mt-0"
          >
          <template #append>
            <StatefulBtn
              @click="projectsStore.save"
              variant="flat"
              icon="mdi-content-save"
              size="small"
            />
            </template>
          </v-combobox>
          <v-list-item
            @click="activeElement = 4"
            key="create-project"
            value="4"
            append-icon="mdi-plus"
          >
            Create Project
          </v-list-item>
          <v-list-item
            v-for="(project, i) in projects"
            @click="activeElement = 4 + i + 1"
            :key="'project' + i"
            :value="4 + i + 1"
          >
            {{ project.name }}
            <template #append>
              <v-btn
                @click="projectStore.del(project.id)"
                icon="mdi-delete"
                elevation="0"
                size="x-small"
                class="mx-0"
                variant="flat"
              />
              <v-btn
                @click="copyProject(project)"
                icon="mdi-content-copy"
                elevation="0"
                size="x-small"
                class="mx-0"
                variant="flat"
              />
            </template>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="10">
        <component
          v-if="activeElement < 4"
          :is="enviroElements[activeElement].form"
        />
        <ProjectForm
          v-else-if="activeElement === 4"
        />
        <ProjectForm
          v-else
          :project="projects[activeProject]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
  
<style scoped>
:deep(.v-combobox > .v-input__append) {
  padding: 0;
}
</style>