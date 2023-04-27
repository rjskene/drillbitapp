<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import MainWindow from '../MainWindow.vue'
import ProjectsTable from './ProjectsTable.vue'
import ProjectsSelectTable from './ProjectsSelectTable.vue'

import { 
 useProjectStore, useProjectsStore,
} from '@/stores/modules'
import { useFormHelpers, useFormatHelpers } from '@/services/composables'

const projectStore = useProjectStore()
const projectsStore = useProjectsStore()
const formHelpers = useFormHelpers()
const format = useFormatHelpers()

const { objects: projects } = storeToRefs(projectStore)
const { object: group } = storeToRefs(projectsStore)
const addProjects = ref(false)
const selected = ref([])
const groupSelected = ref(false)

const filterIds = computed(() => {
  if (!group.value?.projects)
    return []
  return group.value.projects.map((project) => project.id)
})
const disableCreateGroup = computed(() => {
  return groupSelected.value || selected.value.length === 0
})
const createGroup = () => {
  projectsStore.createObjects({
    params: {
      name: projectsStore.object.name,
      project_ids: selected.value,
    } 
  }).then(() => groupSelected.value = true)
}
const deleteGroup = () => {
  projectsStore.deleteObject(group.value.id)
    .then(() => {
      projectsStore.resetObject()
      projectsStore.getObjects()
    })
}
const load = async (params) => {
  if ((typeof params === 'string' || params instanceof String)) {
    projectsStore.$patch((state) => {
      state.object = {name: params}
    })
    groupSelected.value = false
  }
  else if (params) {
    await projectsStore.load(params)
    groupSelected.value = true
  }

}
const addProjectsToGroup = (projectIds) => {
  projectsStore.updateObject({
    pk: group.value.id,
    params: {name: group.value.name, project_ids: projectIds}
  }).then(() => projectsStore.getObject({pk: group.value.id}))
}
const removeProjectsFromGroup = () => {
  projectsStore.updateObject({
    pk: group.value.id,
    params: {
      name: group.value.name, 
      project_ids: selected.value,
      __remove_projects__: true,
    }
  }).then(() => projectsStore.getObject({pk: group.value.id}))
}
</script>

<template>
  <MainWindow>
    <template #nav-panel>
      <v-card-title>Groups</v-card-title>
      <v-combobox
        @update:modelValue="(params) => load(params)"
        @click:clear="projectsStore.resetObject"
        :items="formHelpers.reverse(projectsStore.objects)"
        item-title="name"
        density="compact"
        outlined
        clearable
        class="mt-0 px-3"
      >
        <template v-slot:item="{ item, props }">
          <v-list-item v-bind="props" :disabled="item.raw.disabled">
            <template #subtitle>
              {{format.date(item.raw.created_at)}}
            </template>
          </v-list-item>
        </template>
        <template #append>
          <v-btn
            @click="createGroup"
            :disabled="disableCreateGroup"
            size="large"
            class="ma-0 pa-0 pt-2"
            variant="plain"
            icon="mdi-plus"
          />
          <v-btn
            @click="deleteGroup"
            :disabled="!groupSelected"
            size="large"
            class="ma-0 pa-0 pt-2"
            variant="plain"
            icon="mdi-delete"
          />
        </template>
      </v-combobox>
      <v-slide-y-transition>
        <v-list
          v-if="group"
        >
          <v-list-item
            @click="addProjects = !addProjects"
            variant="flat"
          >Add Projects
            <template #append>
              <v-icon v-if="addProjects" size="large">mdi-chevron-left</v-icon>
              <v-icon v-else size="large">mdi-chevron-right</v-icon>
            </template>
          </v-list-item>
          <v-list-item
            @click="removeProjectsFromGroup"
            :disabled="selected.length === 0"
            variant="flat"
          >Remove Projects
          </v-list-item>
        </v-list>
      </v-slide-y-transition>
    </template>
    <template #main-panel>
      <v-sheet>      
        <ProjectsTable
          @update:selected="(selectedIds) => selected = selectedIds"
          :ids="filterIds"
          class="px-3"
        ></ProjectsTable>
      </v-sheet>
      <v-slide-y-transition>
        <v-sheet
          v-if="addProjects"
          class="px-3 py-6"
        >
          <ProjectsSelectTable
            @select="(selected) => addProjectsToGroup(selected)"
            :ids="filterIds"
            :table-attrs="{height: 400}"
          ></ProjectsSelectTable>
        </v-sheet>
      </v-slide-y-transition>
    </template>
  </MainWindow>
</template>
  
<style scoped>
:deep(.v-combobox > .v-input__append) {
  padding: 0;
}
:deep(.v-btn--icon.v-btn--density-default){
  height: 0 !important;
}
:deep(.v-btn.v-btn--density-default){
  height: 0 !important;
}
</style>