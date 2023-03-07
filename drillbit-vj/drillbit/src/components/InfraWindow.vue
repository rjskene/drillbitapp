<script setup>
import { ref, computed, watch } from 'vue'
import { VBtn } from 'vuetify/components/VBtn'


import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import { FilterMatchMode, FilterOperator } from 'primevue/api'

import CrudTable from './reuseable/CrudTable.vue'
import RejectionCurveBtn from './RejectionCurveBtn.vue'

import { 
  useCoolingStore, useRejectionStore, useElectricalStore,
} from '../stores/modules'
import { useFormatHelpers, TableMaker } from '@/services/composables'
import { useObjectManager } from '../services/composables'

const format = useFormatHelpers()
const crudtable = ref(null)
const tabs = [
  {text: 'Cooling', store: useCoolingStore()},
  {text: 'Heat Rejection', store: useRejectionStore()},
  {text: 'Electrical', store: useElectricalStore()},
]
const currentTab = ref('Heat Rejection')

const tabsObj = computed(() => {
  let obj = {}
  tabs.forEach(tab => {
    obj[tab.text] = tab.store
  })
  return obj
})

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
      bodyFunc: format.power,
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
          minimumFractionDigits: 2,
          suffix: ' x',
          class: 'edit-width-95'
        }
      },
    },
    {
      field: 'price',
      header: 'Price',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-right min-col-width-2dot5 padding-right-1 max-col-width-7',
      bodyFunc: format.currency,
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
  if (currentTab.value === 'Cooling') {
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
  else if (currentTab.value === 'Heat Rejection') {
    cols.splice(2, 0, {
      field: 'design_dry_bulb',
      header: 'Design Dry Bulb',
      headerClass: 'table-header-center max-col-width-7',
      class: 'table-body-center min-col-width-2dot5 max-col-width-7',
      bodyFunc: format.temperature,
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

const tabData = () => {
  return tabsObj.value[currentTab.value].objects
}

const filters = computed(() => {
  let base = {
    'name': {value: null, matchMode: FilterMatchMode.CONTAINS},
    'capacity': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.EQUALS}]}
  }
  if (currentTab.value === 'Heat Rejection') 
    base['design_dry_bulb'] = {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.EQUALS}]}
  
  return base
})
const objManager = ref(useObjectManager({store: tabsObj.value[currentTab.value]}))
watch(currentTab, (currentTab, oldVal) => {
  objManager.value = useObjectManager({store: tabsObj.value[currentTab]})
})
</script>
  
<template>
  <v-card class="ma-12" min-height="1200px">
    <v-tabs
      v-model="currentTab"
      bg-color="background"
    >
      <v-tab
        v-for="tab in tabs"
        :key="tab + '-Tab'"
        :value="tab.text"
        class="tab-color-surface rounded-t-xl"
        slider-color="primary-variant-1"
      >{{ tab.text }}
      </v-tab>
    </v-tabs>
    <v-window
      v-model="currentTab"
      color="surface-lighten-1"
      >
        <v-window-item
          v-for="tab in tabs"
          :key="tab + '-Window'"
          :value="tab.text"
        >
          <v-container>
            <v-row class="d-flex justify-center">
              <v-col cols="10">
                <!-- tabData() is used b/c component data must update BEFORE THE COMPONENT IS RENDERED -->
                <!-- when provided directly, data from other table was sneaking into component -->
                <!-- before columns could update -->
                <CrudTable
                  v-if="tab.store.hasObjects"
                  ref="crudtable"
                  :data="tabData()"
                  :filters="filters"
                  :columns="columns"
                  @undo="objManager.undo()"
                  @redo="objManager.redo()"
                  @delete="({data}) => tab.store.$patch({objects: data})"
                  @save="objManager.save()"
                  :save-state="objManager.saveState"
                  scroll-direction="vertical"
                />
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