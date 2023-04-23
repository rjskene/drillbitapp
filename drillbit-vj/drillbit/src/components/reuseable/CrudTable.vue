<script setup>
import { ref, toRefs, computed, defineProps, defineEmits, defineExpose } from 'vue'
import { useVModel } from '@vueuse/core'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

import CrudActions from './CrudActions.vue'


const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  filters: {
    type: Object,
    default: () => {},
  },
  saveState: {
    type: Object,
    default: () => {},
  },
  paginate: {
    type: Boolean,
    default: true
  },
  edit: {
    type: Boolean,
    default: true
  },
  expansion: {
    type: Boolean,
    default: false
  },
  filterDisplay: {
    type: String,
    default: 'menu'
  },
  scrollDirection: {
    type: String,
    default: 'horizontal'
  },
  loading: {
    type: Boolean,
    default: false,
  }
})

const { data } = toRefs(props)

const dtable = ref(null) // used to access Datatable component refs
const filters = ref(props.filters) // value attribute needs to be changed
const selections = ref([])
const hasSelections = computed(() => selections.value.length > 0)
const editingRows = ref([])

const dtableAttrs = computed(() => {
  let dtableAttrs = {}
  if (props.paginate) {
    dtableAttrs = {
      ...dtableAttrs,
      paginator: true,
      paginatorTemplate: "CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown",
      rowsPerPageOptions: [10,20,50,100],
      currentPageReportTemplate: "Showing {first} to {last} of {totalRecords}",
      rows: 10,
    }
  }
  if (props.edit) {
    dtableAttrs = {
      ...dtableAttrs,
      editMode: "row",
    }
  }
  return dtableAttrs
})
const emit = defineEmits(['add', 'update', 'delete'])
const onRowEditSave = (event) => {
  let { newData } = event
  emit('update', newData)
}
const addNew = () => {
  emit('add')
}
const deleteSelections = () => {
  emit('delete', selections.value)
  selections.value = []
}
defineExpose({dtable})
</script>

<template>
  <CrudActions
    :hasSelections="hasSelections"
    @add="addNew()"
    @delete="deleteSelections()"
    @export:csv="dtable.exportCSV()"
  />
  <DataTable
    ref="dtable"
    dataKey="id"
    :value="data"
    v-model:filters="filters"
    :filterDisplay="props.filterDisplay"
    :showFilterMatchModes="true"
    v-model:selection="selections"
    selectionMode="multiple"
    v-model:editingRows="editingRows"
    @row-edit-save="event => onRowEditSave(event, data)"
    :scrollable="true"
    :scrollDirection="props.scrollDirection"
    sortMode="multiple"
    removableSort
    :loading="loading"
    class="p-datatable-sm mt-3"
    stripedRows
    v-bind="dtableAttrs"
  >
    <Column v-if="props.edit" :rowEditor="true" :exportable="false" frozen/>
    <Column
      v-for="col of columns"
      v-bind="col"
      >
      <template v-if="col.editor" #editor="{data, field}">
        <component
          :is="col.editor.component"
          v-model="data[field]"
          v-bind="col.editor.args"
        />
      </template>
      <template v-if="col.filter" #filter="{filterModel, filterCallback}">
        <component
          v-model="filterModel.value"
          :is="col.filter.component"
          v-bind="col.filter.args"
          @[col.filter.event]="filterCallback()"
        />
      </template>
      <template v-if="col.bodyFunc" #body="{data, field}">
        <span>{{col.bodyFunc(data, field)}}</span>
      </template>
      <template v-else-if="col.spanWrap" #body="{data, field}">
        <span>{{data[field]}}</span>
      </template>
      <template v-else-if="col.component" #body="{data, field}">
        <component
          :is="col.component.component"
          v-bind="col.component.args"
          :id="data.id"
          :key="field + '-' + data.id"
        />
      </template>
    </Column>
    <!-- Expansion column is WRONG; shows button but click doesn't trigger anything -->
    <Column 
      v-if="props.expansion"
      :expander="true"
      headerClass='grc-table-pipeline-expander'
      bodyClass='grc-table-pipeline-expander'
    />
    <template v-if="props.expansion" #expansion="slotProps">
      <slot :props="slotProps" name="expansion">
      </slot> 
    </template>
  </DataTable>
</template>
    
<style scoped>
:deep(.p-datatable-thead > tr > th) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgb(var(--v-theme-background)) !important;
  border-width: 0 0 1px 0 !important;
}
:deep(.p-datatable-tbody > tr > td) {
  border: 1px solid rgb(var(--v-theme-background)) !important;
  border-width: 0 0 1px 0 !important;
}
:deep(.p-datatable-tbody > tr:nth-child(odd)) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: var(--surface-03dp) !important;
}
:deep(.p-datatable-tbody > tr:nth-child(even)) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: var(--surface-02dp) !important;
}
:deep(.p-datatable-tbody > tr.p-highlight) {
    border: 1px solid rgb(var(--v-theme-primary)) !important;
    border-width: 0 0 1px 0 !important;
    background-color: var(--surface-06dp) !important;
    color: white !important;
}
:deep(.p-datatable.p-datatable-hoverable-rows .p-datatable-tbody > tr:not(.p-highlight):hover) {
  color: rgb(var(--v-theme-primary)) !important;
}
:deep(.p-sortable-column-icon) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;  
}
:deep(.p-paginator) {
  background-color: var(--surface-01dp);
}
:deep(.p-paginator > .p-paginator-current) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator > .p-paginator-first) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator > .p-paginator-prev) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator > .p-paginator-pages) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator > .p-paginator-next) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator > .p-paginator-last) {
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
}
:deep(.p-paginator-page.p-highlight) {
  background-color: var(--surface-01dp) !important;
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
  border-color: var(--surface-24dp) !important;
}
:deep(.p-column-filter-row .p-column-filter-menu-button) {
  margin: 0;
}
:deep(.p-column-filter-row .p-column-filter-clear-button) {
  margin: 0;
}
:deep(.p-column-filter-row .p-column-filter-element) {
  width: 100%;
  padding-left: 0px;
  padding-right: 0px;
}
:deep(.p-column-filter-element > .p-inputtext) {
  background-color: var(--surface-01dp);
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
  border-color: rgb(var(--v-theme-background)) !important;
}
:deep(.p-column-filter-row .p-column-filter-element > .p-inputtext) {
  width: 100%;
  padding-top: .1rem;
  padding-bottom: .1rem;
  padding-left: .1rem;
  padding-right: 0px;
}
:deep(.p-column-filter-menu-button.p-column-filter-menu-button-active) {
  background-color: var(--surface-01dp) !important;
  color: rgb(var(--v-theme-secondary)) !important;
  border-color: var(--surface-24dp) !important;
}
:deep(.p-cell-editing > .p-inputtext) {
  padding: .1rem 0 .1rem .1rem;
}
:deep(.p-cell-editing > .p-inputtext) {
  background-color: var(--surface-01dp) !important;
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
  border-color: var(--surface-24dp) !important;
}
:deep(.p-inputnumber-input) {
  padding: .1rem 0 .1rem .1rem;
  background-color: var(--surface-01dp) !important;
  color: rgb(var(--v-theme-on-surface-01dp)) !important;
  border-color: var(--surface-24dp) !important;
}
:deep(.p-frozen-column) {
  max-width: 3rem;
}
:deep(.p-column-filter-row) {
  width: 75%;
}


:deep(.edit-width-50.p-inputnumber) {
  width: 50%;
}
:deep(.edit-width-50 > .p-inputtext) {
  width: 50%;
}
:deep(.edit-width-75.p-inputnumber) {
  width: 50%;
}
:deep(.edit-width-75 > .p-inputtext) {
  width: 50%;
}
:deep(.edit-width-90.p-inputnumber) {
  width: 90%;
}
:deep(.edit-width-90 > .p-inputtext) {
  width: 90%;
}
:deep(.edit-width-95.p-inputnumber) {
  width: 95%;
}
:deep(.edit-width-95 > .p-inputtext) {
  width: 95%;
}
</style>