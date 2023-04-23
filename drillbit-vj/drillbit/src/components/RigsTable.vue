<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState } from '@vueuse/core'

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import { FilterMatchMode } from 'primevue/api'

import CrudTable from '../components/reuseable/CrudTable.vue'

import { useFormatHelpers, TableMaker } from '@/services/composables'

import { useRigStore } from '../stores/modules'

const rigStore = useRigStore()
const format = useFormatHelpers()

const columns = computed(() => {
  let cols = [
  {
    field: 'make',
    header: 'Make', 
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    sortable: true,
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
    sortable: true,
    editor: {
      component: InputText,
      args: {
        type: 'text',
      }
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
    sortable: true,
    editor: {
      component: InputText,
      args: {
        type: 'text',
      }
    },
  },
  {
    field: 'manufacturer',
    header: 'Manufacturer',
    headerClass: 'table-header-center min-col-width-10',
    bodyClass: 'table-body-center min-col-width-10',
    sortable: true,
    editor: {
      component: InputText,
      args: {
        type: 'text',
      }
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
    sortable: true,
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
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.power(data[field], {toFixed: 2}),
    sortable: true,
    editor: {
      component: InputNumber,
      args: {
        suffix: " W"
      }
    },
  },
  {
    field: 'efficiency',
    header: 'Efficiency',
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.efficiency(data[field], {toFixed: 1}),
    sortable: true,
  },
  {
    field: 'buffer',
    header: 'Buffer',
    headerClass: 'table-header-center min-col-width-2dot5',
    bodyClass: 'table-body-center min-col-width-2dot5',
    bodyFunc: (data, field) => format.percentage(data[field]),
    sortable: true,
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
    headerClass: 'table-header-center',
    bodyClass: 'table-body-right min-col-width-2dot5 padding-right-1',
    bodyFunc: (data, field) => format.currency(data[field]),
    sortable: true,
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

const { objects } = storeToRefs(rigStore)
const state = ref(null)
const loading = computed(() => { 
  return state.value !== null ? false : state.value?.isLoading
})

const addRig = () => {
  let add = rigStore.createObjects({
    params: {
      buffer: 0,
      hash_rate: 0,
      power: 0,
  }}).then(() => {
    rigStore.getObjects()
  })
  state.value = useAsyncState(add)
}
const updateRig = (data) => {
  let update = rigStore.updateObject({
      pk: data.id,
      params: data,
    }).then(() => {
      rigStore.getObjects()
    })
  state.value = useAsyncState(update)
}
const deleteRig = (data) => {
  let pk = data.map(data => data.id)
  let deleteFunc = rigStore
    .deleteObject(pk)
    .then(() => {
      rigStore.getObjects()
  })
  state.value = useAsyncState(deleteFunc)
}
</script>

<template>
  <CrudTable
    v-if="objects"
    @add="addRig()"
    @update="(data) => updateRig(data)"
    @delete="(data) => deleteRig(data)"
    :data="objects"
    :filters="filters"
    :columns="columns"
    :loading="loading"
  >
  </CrudTable>
</template>  
  
<style scoped>
  
</style>