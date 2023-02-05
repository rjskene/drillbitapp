<script setup>
import { ref, computed } from 'vue'

import ProjectForm from './ProjectForm.vue'

import BlockScheduleForm from './BlockScheduleForm.vue'
import BTCPriceForm from './BTCPriceForm.vue'
import TransactionFeesForm from './TransactionFeesForm.vue'
import NetworkHashRateForm from './NetworkHashRateForm.vue'

import { 
  useBlockScheduleStore, useBTCPriceStore, useFeeStore, useHashRateStore,
  useProjectStore, useInputStore,
} from '../stores/modules'

const projectStore = useProjectStore()
const inputStore = useInputStore()
const activeElement = ref(0)

const enviroElements = [
  {text: 'Block Schedule', value: 0, form: BlockScheduleForm, store: useBlockScheduleStore()},
  {text: 'BTC Price', value: 1, form: BTCPriceForm, store: useBTCPriceStore()},
  {text: 'Transaction Fees', value: 2, form: TransactionFeesForm, store: useFeeStore()},
  {text: 'Network Hash Rate', value: 3, form: NetworkHashRateForm, store: useHashRateStore()}
]

const readyOrNot = (item) => {
  if (item.store) {
    return {
      icon: inputStore.locked[item.store.$id.replace('Store', '')] ? 'mdi-check' : 'mdi-close',
      color: inputStore.locked[item.store.$id.replace('Store', '')] ? 'secondary' : 'error'
    }
  }
  return {}
}
const projectFormProps = computed(() => {
  if (activeElement.value > 4) {
    return {
      project: projectStore.projects[activeElement.value - 5]
    }
  }
  return null
})
const deleteProject = (index) => {
  projectStore.$patch((state) => {
    state.projects.pop(index)
  })
}
</script>

<template>
  <v-container fluid class="">
    <v-row>
      <v-col cols="2">
        <v-list
          nav
          density="compact"
        >
          <v-list-subheader class="text-subtitle-1">Environment</v-list-subheader>
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
          <v-list-item
            @click="activeElement = 4"
            key="create-project"
            value="4"
            append-icon="mdi-plus"
          >
            Create Project
          </v-list-item>
          <v-list-item
            v-for="(project, i) in projectStore.projects"
            @click="activeElement = 4 + i + 1"
            :key="'project' + i"
            :value="4 + i + 1"
          >
            {{ project.name }}
            <template #append>
              <v-btn
                @click="deleteProject(i)"
                icon="mdi-delete"
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
          v-else-if="projectFormProps === null"
        />
        <ProjectForm
          v-else
          v-bind="projectFormProps"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
  
  
<style scoped>
</style>