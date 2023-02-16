<script setup>
import { ref, computed, watch } from 'vue'

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import { FilterMatchMode } from 'primevue/api'

import CrudTable from './reuseable/CrudTable.vue'

import { 
  useCoolingStore, useRejectionStore, useElectricalStore,
} from '../stores/modules'
import { useFormatHelpers, TableMaker } from '@/services/composables'
import { useObjectManager } from '../services/composables'

const format = useFormatHelpers()
const tabs = [
  {text: 'Cooling', store: useCoolingStore()},
  {text: 'Heat Rejection', store: useRejectionStore()},
  {text: 'Electrical', store: useElectricalStore()},
]
const currentTab = ref('Cooling')

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
      headerClass: 'table-header-center',
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
          // class: 'p-inputtext-sm min-col-width-5',
        }
      }
    },
    {
      field: 'power',
      header: 'Power',
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-2dot5',
      bodyFunc: format.power,
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          suffix: ' W',
        }
      },
    },
    {
      field: 'pue',
      header: 'PUE',
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-2dot5',
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          minimumFractionDigits: 2,
          suffix: ' x',
        }
      },
    },
    {
      field: 'number_of_rigs',
      header: 'Rigs',
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-2dot5',
      editor: {
        component: InputNumber,
        args: {
          mode: 'decimal',
          locale: "en-US",
          minimumFractionDigits: 2,
        }
      },
    },
    {
      field: 'price',
      header: 'Price',
      headerClass: 'table-header-center',
      bodyClass: 'table-body-right min-col-width-2dot5 padding-right-1',
      bodyFunc: format.currency,
      editor: {
        component: InputNumber,
        args: {
          mode: 'currency',
          locale: "en-US",
          currency: 'USD'
        }
      },
    },
  ]
  let table = new TableMaker(cols)
  return table.columns
})

const filters = {
  'name': {value: null, matchMode: FilterMatchMode.CONTAINS},
}
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
          <CrudTable
            v-if="tab.store.hasObjects"
            ref="crudtable"
            :data="tab.store.objects"
            :filters="filters"
            :columns="columns"
            @undo="objManager.undo()"
            @redo="objManager.redo()"
            @delete="({data}) => tab.store.$patch({objects: data})"
            @save="objManager.save()"
            :save-state="objManager.saveState"
          />
        </v-window-item>
      </v-window>
  </v-card>
</template>
  
<style scoped>
:deep(.tab-color-surface) {
  background-color: rgb(var(--v-theme-surface));

}
</style>