<script setup>
import { ref, computed, watch } from 'vue'
import { useAsyncState } from '@vueuse/core'

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import { FilterMatchMode, FilterOperator } from 'primevue/api'

import CrudTable from './reuseable/CrudTable.vue'
import RejectionCurveBtn from './RejectionCurveBtn.vue'

import { 
  useCoolingStore, useRejectionStore, useElectricalStore,
} from '../stores/modules'
import { useFormatHelpers, TableMaker } from '@/services/composables'

const format = useFormatHelpers()

const tabs = [
  {text: 'Cooling', store: useCoolingStore()},
  {text: 'Heat Rejection', store: useRejectionStore()},
  {text: 'Electrical', store: useElectricalStore()},
]
const currentTab = ref(0)
const data = ref(tabs[0].store.objects)
const tab = computed(() => {return tabs[currentTab.value]})
const store = computed(() => {return tab.value?.store})

const updateData = () => {
  data.value = store.value.objects
}

const state = ref(null)
const loading = computed(() => { 
  return state.value !== null ? false : state.value?.isLoading
})

const defaults = [
  {price: 0 , pue: 0},
  {price: 0 , pue: 0},
]
const defaultParams = computed(() => {
  return defaults[currentTab.value]
})

const addInfra = () => {
  let add = store.value.createObjects({
    params: defaultParams.value}).then(() => {
    store.value.getObjects().then(() => {
      updateData()
    })
  })
  state.value = useAsyncState(add)
}
const updateInfra = (data) => {
  let update = store.value.updateObject({
      pk: data.id,
      params: data,
    }).then(() => {
      store.value.getObjects().then(() => {
        updateData()
    })
    })
  state.value = useAsyncState(update)
}
const deleteInfra = (data) => {
  let pk = data.map(data => data.id)
  let deleteFunc = store.value
    .deleteObject(pk)
    .then(() => {
      store.value.getObjects().then(() => {
        updateData()
    })
  })
  state.value = useAsyncState(deleteFunc)
}

const columns = computed(() => {
  let cols = [
    {
      field: 'name',
      header: 'Name', 
      headerClass: 'table-header-left',
      class: 'table-body-left min-col-width-10',
      editor: {
        component: InputText,
      },
      filter: {
        component: InputText,
        event: 'input',
        args: {
          type: 'text',
          placeholder: 'Search',
        }
      }
    },
    {
      field: 'capacity',
      header: 'Capacity',
      dataType: 'numeric',
      headerClass: 'table-header-center min-col-width-2dot5 max-col-width-7',
      class: 'table-body-center min-col-width-2dot5 max-col-width-7',
      bodyFunc: (data, field) => format.power(data[field]),
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          suffix: ' W',
          class: 'edit-width-95'
        }
      },
      filter: {
        component: InputNumber,
        event: 'input',
        args: {
          mode: 'decimal',
          locale: "en-US",
          placeholder: 'Search',
        }
      }
    },
    {
      field: 'pue',
      header: 'PUE',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-center min-col-width-2dot5 max-col-width-7',
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          minFractionDigits: 2,
          class: 'edit-width-95'
        }
      },
    },
    {
      field: 'price',
      header: 'Price',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-right min-col-width-2dot5 padding-right-1 max-col-width-7',
      bodyFunc: (data, field) => format.currency(data[field]),
      editor: {
        component: InputNumber,
        args: {
          mode: 'currency',
          locale: "en-US",
          currency: 'USD',
          class: 'edit-width-95'
        }
      },
    },
  ]
  if (currentTab.value === 0) {
    cols.splice(2, 0, {
      field: 'number_of_rigs',
      header: 'Rigs',
      headerClass: 'table-header-center',
      class: 'table-body-center min-col-width-2dot5',
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          minimumFractionDigits: 2,
          class: 'edit-width-75'
        }
      },
    }
    )
  }
  else if (currentTab.value === 1) {
    cols.splice(2, 0, {
      field: 'design_dry_bulb',
      header: 'Design Dry Bulb',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-center min-col-width-2dot5 max-col-width-7',
      bodyFunc: (data, field) => format.temperature(data[field]),
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          suffix: ' °F',
          class: 'edit-width-95'
        }
      },
      filter: {
        component: InputNumber,
        event: 'input',
        args: {
          mode: 'decimal',
          locale: "en-US",
          placeholder: 'Search',
        }
      }
    }, 
    {
      field: 'curve',
      header: 'Curve',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-center min-col-width-2dot5 max-col-width-7',
      component: {
        component: RejectionCurveBtn,
        props: {
          pk: (data, field) => data.id,
        },
        args: {
          color: 'surface'
        }
      },
    }
    )
  }
  let table = new TableMaker(cols)
  
  return table.columns
})
const filters = computed(() => {
  let base = {
    'name': {value: null, matchMode: FilterMatchMode.CONTAINS},
    'capacity': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.EQUALS}]}
  }
  if (currentTab.value === 1) 
    base['design_dry_bulb'] = {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.EQUALS}]}
  
  return base
})
</script>
  
<template>
  <v-card class="mx-10 my-5" min-height="1200px">
    <v-tabs
      v-model="currentTab"
      bg-color="background"
    >
      <v-tab
        v-for="(tab, i) in tabs"
        :key="tab + '-Tab'"
        :value="i"
        class="tab-color-surface rounded-t-xl"
        slider-color="primary-variant-1"
      >
        {{ tab.text }}
      </v-tab>
    </v-tabs>
    <v-window
      v-model="currentTab"
      color="surface-lighten-1"
      >
        <v-window-item
          v-for="(tab, i) in tabs"
          :key="tab + '-Window'"
          :value="i"
        >
          <v-container>
            <v-row class="d-flex justify-center">
              <v-col cols="10">
                <!-- tabData() is used b/c component data must update BEFORE THE COMPONENT IS RENDERED -->
                <!-- when provided directly, data from other table was sneaking into component -->
                <!-- before columns could update -->
                <CrudTable
                  v-if="data"
                  @add="addInfra()"
                  @update="(data) => updateInfra(data)"
                  @delete="(data) => deleteInfra(data)"
                  :data="data"
                  :filters="filters"
                  :columns="columns"
                  :loading="loading"
                />
                {{ data }}
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>
      </v-window>
  </v-card>
</template>
  
<style scoped>
:deep(.tab-color-surface) {
  background-color: rgb(var(--v-theme-surface));

}

</style>