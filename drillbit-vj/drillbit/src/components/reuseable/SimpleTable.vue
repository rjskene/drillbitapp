<script setup>
import { ref, toRefs, computed, defineProps, defineEmits, defineExpose } from 'vue'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
})
const { name, data } = toRefs(props)  // data is a reactive ref
const dtable = ref(null) // used to access Datatable component refs

</script>

<template>
  <DataTable
    ref="dtable"
    dataKey="id"
    :value="data"
    rowGroupMode="subheader" 
    groupRowsBy="product"
    class="p-datatable-sm mt-3"
    stripedRows
  >
    <Column
      v-for="col of columns"
      :field="col.field"
      :header="col.header"
      :headerClass="col.headerClass"
      :class="col.bodyClass"
      :key="col.field"
    >
      <template v-if="col.bodyFunc" #body="{data, field}">
          <span>{{col.bodyFunc(data[field])}}</span>
      </template>
      <template v-if="col.bodyFuncWithDataAccess" #body="{data, field}">
        <slot name="bodyFunc" :col="col" :data="data" :field="field">
          <span>{{col.bodyFuncWithDataAccess(data, field)}}</span>
        </slot>
      </template>
      <template v-else-if="col.spanWrap" #body="{data, field}">
        <span>{{data[field]}}</span>
      </template>
    </Column>
  </DataTable>
</template>
  
<style scoped>
  :deep(.p-datatable-thead > tr > th) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: rgba(var(--v-theme-surface-01dp)) !important;
  border: 1px solid rgba(var(--v-border-color), .05) !important;
  border-width: 1px 0 1px 0 !important;
}
:deep(.p-datatable-thead > tr > th:first-child) {
  border-width: 1px 0 1px 1px !important;
}
:deep(.p-datatable-thead > tr > th:last-child) {
  border-width: 1px 1px 1px 0 !important;
}
:deep(.p-datatable-tbody > tr > td) {
  border: 1px solid rgba(var(--v-border-color), .05) !important;
  border-width: 0 0 1px 0 !important;
}
:deep(.p-datatable-tbody > tr > td:first-child) {
  border-width: 1px 0 1px 1px !important;
}
:deep(.p-datatable-tbody > tr > td:last-child) {
  border-width: 1px 1px 1px 0 !important;
}
:deep(.p-datatable-tbody > tr:nth-child(odd)) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: rgba(var(--v-theme-surface)) !important;
}
:deep(.p-datatable-tbody > tr:nth-child(even)) {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  background-color: rgba(var(--v-theme-surface-01dp), 1) !important;
}
:deep(.p-datatable-tbody > tr.p-highlight) {
    border: 1px solid rgb(var(--v-theme-primary)) !important;
    border-width: 0 0 1px 0 !important;
    background-color: var(--surface-01dp) !important;
    color: white !important;
}
</style>