<script setup>
import { ref, computed, watchEffect, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState } from '@vueuse/core'
import { useRefHistory } from '@vueuse/core'

import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import { FilterMatchMode } from 'primevue/api'

import CrudTable from '../components/reuseable/CrudTable.vue'

import { useFormatHelpers, TableMaker } from '@/services/composables'

import { useRigStore } from '../stores/modules'

const rigStore = useRigStore()
const format = useFormatHelpers()
const crudtable = ref(null)

const columns = computed(() => {
  let cols = [
  {
    field: 'make',
    header: 'Make', 
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    editor: {
      component: InputText,
    },
    filter: {
      component: InputText,
      event: 'input',
      args: {
        type: 'text',
        placeholder: 'Search',
        class: 'p-inputtext-sm min-col-width-5',
      }
    }
  },
  {
    field: 'model',
    header: 'Model',
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    editor: {
      component: InputText,
    },
    filter: {
      component: InputText,
      event: 'input',
      args: {
        type: 'text',
        placeholder: 'Search',
        class: 'p-inputtext-sm',
      }
    }
  },
  {
    field: 'generation',
    header: 'Generation',
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    editor: {
      component: InputText,
    },
  },
  {
    field: 'manufacturer',
    header: 'Manufacturer',
    headerClass: 'table-header-center min-col-width-10',
    bodyClass: 'table-body-center min-col-width-10',
    editor: {
      component: InputText,
    },
    filter: {
      component: InputText,
      event: 'input',
      args: {
        type: 'text',
        placeholder: 'Search',
        class: 'p-inputtext-sm',
      }
    }
  },
  {
    field: 'hash_rate',
    header: 'Hash Rate',
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.hashRate(data[field]),
    editor: {
      component: InputNumber,
      args: {
        suffix: " TH/s"
      }
    },
  },
  {
    field: 'power',
    header: 'Power',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.power(data[field]),
    editor: {
      component: InputNumber,
      args: {
        suffix: " W"
      }
    },
  },
  {
    field: 'buffer',
    header: 'Buffer',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-2dot5',
    bodyFunc: (data, field) => format.percentage(data[field]),
    editor: {
      component: InputNumber,
      args: {
        minimumFractionDigits: 4,
      }
    },
  },
  {
    field: 'price',
    header: 'Price',
    headerClass: 'table-header-center pl-12',
    bodyClass: 'table-body-right min-col-width-2dot5 padding-right-1',
    bodyFunc: (data, field) => format.currency(data[field]),
    editor: {
      component: InputNumber,
      args: {
        mode: 'currency',
        currency: 'USD'
      }
    },
  },
]
  let table = new TableMaker(cols)
  return table.columns
})

const filters = {
  'make': {value: null, matchMode: FilterMatchMode.CONTAINS},
  'model': {value: null, matchMode: FilterMatchMode.CONTAINS},
  'manufacturer': {value: null, matchMode: FilterMatchMode.CONTAINS},
}
const { state, isReady, isLoading, error } = useAsyncState(() => rigStore.getObjects())

const saveState = ref(null)
const saveRigs = () => { saveState.value = useAsyncState(() => rigStore.updateObjects()) }

const rigs = ref([])
watchEffect(() => {
  if (isReady.value) {
    rigs.value = rigStore.objects
  }
})
const { history, undo, redo } = useRefHistory(rigs, {deep: true})

watch(rigs, (newVal, oldVal) => {
  rigStore.$patch({objects: newVal})
})

</script>

<template>
  <CrudTable
    v-if="rigStore.hasObjects"
    ref="crudtable"
    :data="rigStore.objects"
    :filters="filters"
    :columns="columns"
    @undo="undo"
    @redo="redo"
    @delete="({data}) => rigStore.$patch({objects: data})"
    @save="saveRigs()"
    :save-state="saveState"
  >
  </CrudTable>
</template>  
  
<style scoped>
  
</style>