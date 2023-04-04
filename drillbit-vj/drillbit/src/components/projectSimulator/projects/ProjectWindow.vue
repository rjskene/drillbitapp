<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import MainWindow from '../MainWindow.vue'
import ProjectForm from './ProjectForm.vue'

import { 
 useProjectStore, useProjectsStore,
} from '@/stores/modules'
import { useFormHelpers } from '@/services/composables'

const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const formHelpers = useFormHelpers()

const { projects } = storeToRefs(projectStore)

const activeIndex = ref(0)

const load = async (params) => {
  console.log('load', params)
  if ((typeof params === 'string' || params instanceof String))
    projectsStore.$patch((state) => {
      state.object = {name: params}
    })
  else if (params)
    await projectsStore.load(params)
}
const copy = (project) => {
  const {['id']: _, ...params} = project
  projectStore.create(params)
}
</script>

<template>
  <MainWindow>
    <template #nav-panel>
      <v-combobox
        @update:modelValue="(params) => load(params)"
        @click:clear="projectsStore.resetObject"
        :items="formHelpers.reverse(projectsStore.objects)"
        :rules="formHelpers.nameRules.value"
        item-title="name"
        label="Projects"
        density="compact"
        outlined
        clearable
        class="mt-0 pl-3"
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
        @click="activeIndex = -1"
        key="create-project"
        value="4"
        append-icon="mdi-plus"
        class="pl-3 pr-2"
      >
        Create Project
      </v-list-item>
      <v-list-item
        v-for="(project, i) in projects"
        @click="activeIndex = i"
        :key="'project' + i"
        :value="i"
        class="pl-3 pr-1"
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
            @click="copy(project)"
            icon="mdi-content-copy"
            elevation="0"
            size="x-small"
            class="mx-0"
            variant="flat"
          />
        </template>
      </v-list-item>
    </template>
    <template #main-panel>
      <ProjectForm
        v-if="activeIndex === -1"
      />
      <ProjectForm
        v-else
        :project="projects[activeIndex]"
      />
    </template>
  </MainWindow>
</template>
  
<style scoped>
:deep(.v-combobox > .v-input__append) {
  padding: 0;
}
</style>