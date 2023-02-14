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
  // saveState: {
  //   type: Object,
  //   default: () => {},
  // },
  // paginate: {
  //   type: Boolean,
  //   default: true
  // },
  // edit: {
  //   type: Boolean,
  //   default: true
  // },
  // expansion: {
  //   type: Boolean,
  //   default: false
  // },
})
const { name, data } = toRefs(props)  // data is a reactive ref
const dtable = ref(null) // used to access Datatable component refs

// const dtableAttrs = computed(() => {
//   let dtableAttrs = {}
//   if (props.paginate) {
//     dtableAttrs = {
//       ...dtableAttrs,
//       paginator: true,
//       paginatorTemplate: "CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown",
//       rowsPerPageOptions: [10,20,50,100],
//       currentPageReportTemplate: "Showing {first} to {last} of {totalRecords}",
//       rows: 10,
//     }
//   }
//   if (props.edit) {
//     dtableAttrs = {
//       ...dtableAttrs,
//       editMode: "row",
//     }
//   }
//   return dtableAttrs
// })

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
        <slot name="bodyFunc" :col="col" :data="data" :field="field">
          <span>{{col.bodyFunc(data[field])}}</span>
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
:deep(.p-cell-editing.p-frozen-column) {
  width: 425px;
}
</style>