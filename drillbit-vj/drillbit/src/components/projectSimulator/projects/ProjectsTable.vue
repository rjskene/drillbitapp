<script setup>
import { computed, ref, toRefs, watch} from 'vue'

import { storeToRefs } from 'pinia'
import { useVModel, useAsyncState } from '@vueuse/core'

import { VDataTable } from 'vuetify/labs/VDataTable'
import ProjectForm from './ProjectForm.vue'

import { useFormatHelpers, TableMaker } from '@/services/composables'
import { useProjectStore, useProjectsStore } from '@/stores/modules'

const format = useFormatHelpers()
const projStore = useProjectStore()

const emit = defineEmits(['update:selected'])
const props = defineProps({
  ids: {
    type: Array,
    default: [],
  },
})
const { ids } = toRefs(props)
const { objects: projects } = storeToRefs(projStore)

const dtable = ref(null)
const showProjectForm = ref(false)
const selected = ref([])
const expanded = ref([])

const emitSelected = () => {
  emit('update:selected', selected.value)
}
watch(selected, emitSelected)

const itemManager = (data, column) => {
  if (column.bodyFunc)
    return column.bodyFunc(data, column.key)
  else
    return data[column.key]
}

const state = ref(null)
const createProject = () => {
  let create = projStore.createObjects({
    params: {
      name: 'New Project',
      ambient_temp_source: null,
      target_ambient_temp: null,
    }
  })
  state.value = useAsyncState(
    create, 
    {},
    {
      onError: (err) => {
        console.error(err)
      },
    }
  )
  showProjectForm.value = true
}
const editProject = (pk) => {
  let edit = projStore.getObject({pk})
  state.value = useAsyncState(
    edit, 
    {},
    {
      onError: (err) => {
        console.error(err)
      },
    }
  )
  showProjectForm.value = true
}
const deleteProject = (pk) => {
  projStore.deleteObject(pk)
    .then(() => projStore.getObjects())
}
const filterIds = (value, query, item) => { 
  let filterIds = JSON.parse(query)
  if (filterIds.length == 0)
    return true
  return filterIds.includes(item.value)
}
const columns = computed(() => {
  let cols = [
    {
      key: 'actions',
      align: 'middle',
      width: '7%',
      sortable: false,
    },
    {
      key: 'id',
      title: 'ID', 
      align: 'start',
      sortable: true,
    },
    {
      key: 'name',
      title: 'Name',
      align: 'start',
      sortable: true,
    },
    {
      key: 'capacity',
      title: 'Capacity',
      bodyFunc: (data, field) => format.power(data[field], {toFixed: 2}),
      align: 'center',
      sortable: true,
    },
    {
      key: 'energy_price',
      title: 'Energy Price',
      bodyFunc: (data, field) => format.energyPrice(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'target_overclocking',
      title: 'Overclock',
      bodyFunc: (data, field) => data[field] + 'x',
      align: 'center',
      sortable: true,
    },
    {
      key: 'pool_fees',
      title: 'Pool Fees',
      bodyFunc: (data, field) => format.percentage(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'created_at',
      title: 'Created',
      bodyFunc: (data, field) => format.date(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'updated_at',
      title: 'Last Updated',
      bodyFunc: (data, field) => format.date(data[field]),
      align: 'center',
      sortable: true,
    },
  ]
  let table = new TableMaker(cols)
  return table.columns
})
</script>
  
  
<template>
      <!-- :sort-by="[{ key: 'updated_at', order: 'desc' }]" -->
  <v-data-table
    ref="dtable"
    v-model="selected"
    v-model:expanded="expanded"
    :custom-filter="filterIds"
    :search="JSON.stringify(ids)"
    :headers="columns"
    :items="projects"
    item-title="name"
    density="compact"
    show-select
    show-expand
    multi-sort
    class="ma-0"
  >
    <template #top>
      <v-toolbar
        color="surface"
        class="ma-0"
      >
        <v-toolbar-title>
          Projects
        </v-toolbar-title>
        <v-icon
          @click="createProject"
          size="large"
          class="pr-6"
        >
          mdi-plus
        </v-icon>
      </v-toolbar>
      <v-dialog
        v-model="showProjectForm"
        transition="dialog-bottom-transition"
        min-width="100px"
      >
        <v-icon
          @click="showProjectForm = false"
          
          size="large"
          class="pt-3"
        >
          mdi-close
        </v-icon>
        <v-card
          class="pa-4 rounded-xl"
        >
          <v-progress-circular
            v-if="state?.isLoading"
          ></v-progress-circular>
          <ProjectForm
            v-else
            :project="projStore.object"
          ></ProjectForm>
        </v-card>
      </v-dialog>

    </template>
    <template #item.actions="{ item}">
      <v-icon
        size="small"
        class="me-2"
        @click="editProject(item.raw.id)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        size="small"
        @click="deleteProject(item.raw.id)"
      >
        mdi-delete
      </v-icon>

    </template>
    <template
      v-for="column in columns.slice(1, columns.length)"
      v-slot:[`item.${column.key}`]="{ item }"
    >
      {{ itemManager(item.raw, column) }}
    </template>
    <template v-slot:expanded-row="{ columns, item }">
      <tr>
        <td :colspan="columns.length">
          <v-card
            color="surface-02dp"
            elevation="0"
            class="rounded-xl my-6 pa-6"
          >
            <v-card-title class="ml-0 pl-0">Details</v-card-title>
            <v-row class="pt-3">
              <v-col>
                <span class="text-subtitle-1">Rigs</span>
              </v-col>
            </v-row>
            <v-row 
              v-if="item.raw.rigs.length > 0"
              class="d-flex justify-space-between">
              <v-col class="d-flex align-center pl-3 pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Name:</span>
                {{item.raw.rigs[0].rig.name}}
              </v-col>
              <v-col class="d-flex align-center pl-3 pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Power:</span>
                {{format.power(item.raw.rigs[0].rig.power, { toFixed: 2 })}}
              </v-col>
              <v-col class="d-flex align-center pl-3 pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">HR:</span>
                {{format.hashRate(item.raw.rigs[0].rig.hash_rate)}}
              </v-col>
              <v-col class="d-flex align-center pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Price:</span>
                {{ format.currency(item.raw.rigs[0].price) }}
              </v-col>
              <v-col class="d-flex align-center pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Quantity:</span>
                {{ item.raw.rigs[0].quantity }}
              </v-col>
              <v-col class="d-flex align-center pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Total Cost:</span>
                {{format.currency(item.raw.rigs[0].quantity * item.raw.rigs[0].price)}}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <span class="text-subtitle-1">Infrastructure</span>
              </v-col>
            </v-row>
            <v-row
              v-for="infra in item.raw.infrastructure"
              class="d-flex justify-space-between"
            >
              <v-col class="d-flex align-center pl-3 pr-0 pt-0 ml-0 mr-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Power:</span>
                {{ format.power(infra.infrastructure.capacity) }}
              </v-col>
              <v-col class="d-flex align-center pl-1 pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">PUE:</span>
                {{infra.infrastructure.pue}}x
              </v-col>
              <v-col class="d-flex align-center pl-0 pr-0 pt-0 ml-0 mr-0">
                <span class="text-body-2 text-medium-emphasis pl-0 ml-0">Price:</span>
                {{ format.currency(infra.price) }}
              </v-col>
              <v-col class="d-flex align-center pl-1 pr-0 pt-0 ml-0 mr-0">
                <span class="text-body-2 text-medium-emphasis">Quantity:</span>
                {{ infra.quantity }}
              </v-col>
              <v-col class="d-flex align-center pt-0">
                <span class="text-body-2 text-medium-emphasis mr-1">Total Cost:</span>
                {{format.currency(infra.quantity * infra.price)}}
              </v-col>
            </v-row>
          </v-card>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>
  
  
<style scoped>
  
</style>