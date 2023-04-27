<script setup>
import { computed, ref, toRefs, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState } from '@vueuse/core'

import { VDataTableVirtual } from 'vuetify/labs/VDataTable'

import { useFormatHelpers, TableMaker } from '@/services/composables'
import { useProjectStore, useProjectsStore } from '@/stores/modules'

const format = useFormatHelpers()
const projStore = useProjectStore()

const emit = defineEmits(['select'])
const props = defineProps({
  ids: {
    type: Array,
    default: [],
  },
  tableAttrs: {
    type: Object,
    default: () => ({}),
  }
})
const { ids } = toRefs(props)
const { objects: projects } = storeToRefs(projStore)

const showProjectForm = ref(false)
const selected = ref([])
const expanded = ref([])

const columns = computed(() => {
  let cols = [
    {
      key: 'id',
      align: 'start',
      sortable: true,
    },
    {
      key: 'name',
      align: 'start',
      sortable: true,
    },
    {
      key: 'capacity',
      bodyFunc: (data, field) => format.power(data[field], {toFixed: 2}),
      align: 'center',
      sortable: true,
    },
    {
      key: 'energy_price',
      bodyFunc: (data, field) => format.energyPrice(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'target_overclocking',
      bodyFunc: (data, field) => data[field] + 'x',
      align: 'center',
      sortable: true,
    },
    {
      key: 'pool_fees',
      bodyFunc: (data, field) => format.percentage(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'created_at',
      bodyFunc: (data, field) => format.date(data[field]),
      align: 'center',
      sortable: true,
    },
    {
      key: 'updated_at',
      bodyFunc: (data, field) => format.date(data[field]),
      align: 'center',
      sortable: true,
    },
  ]
  let table = new TableMaker(cols)
  return table.columns
})
const itemManager = (data, column) => {
  if (column.bodyFunc)
    return column.bodyFunc(data, column.key)
  else
    return data[column.key]
}
const filterIds = (value, query, item) => { 
  let filterIds = JSON.parse(query)
  if (filterIds.length == 0)
    return true
  return !filterIds.includes(item.value)
}
const emitSelect = () => {
  emit('select', selected.value)
}
watch(selected, emitSelect)
</script>
  
  
<template>
  <v-data-table-virtual
    v-model="selected"
    v-bind="tableAttrs"
    :custom-filter="filterIds"
    :search="JSON.stringify(ids)"
    :headers="columns"
    :items="projects"
    :sort-by="[{ key: 'updated_at', order: 'desc' }]"
    item-title="name"
    density="compact"
    show-select
    multi-sort
    class="ma-0"
  >
    <template
      v-for="column in columns.slice(1, columns.length)"
      v-slot:[`item.${column.key}`]="{ item }"
    >
      {{ itemManager(item.raw, column) }}
    </template>
  </v-data-table-virtual>
</template>
  
  
<style scoped>
  
</style>