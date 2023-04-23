<script setup>
import { ref, toRefs, computed, defineProps, onBeforeMount, watch } from 'vue'
import { useAsyncState } from '@vueuse/core'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import { useFormatHelpers, NewTableMaker } from '@/services/composables'
import { useStatementStore } from '@/stores/modules'

const statStore = useStatementStore()
const format = useFormatHelpers()

const props = defineProps(
  {
    sim: {
      type: Object,
      required: true
    },
  }
)
const { sim } = toRefs(props)
const statObject = ref(null)
const freqIndex = ref(2)
const statState = ref(null)

const loadStatObject = (index) => {
  statState.value = useAsyncState(
    statStore
      .getObjects({sim: sim.value.id, frequency: statStore.allowedFreqs[index]})
      .then( () => {
        statObject.value = statStore.objects[0]
      }
    ),
    {},
    {
      onError: (error) => {
        console.error(error.response ?? error)
      }
    }
  )
}

onBeforeMount(() => loadStatObject(freqIndex.value))
watch(() => freqIndex.value, (newVal, oldVal) => {
  loadStatObject(newVal)
})
watch(() => sim.value, (newVal, oldVal) => {
  loadStatObject(freqIndex.value)
})

const statTypes = [
  {value: 'env', icon: 'earth'}, 
  {value: 'istat', icon: 'cash'}, 
  {value: 'roi', icon: 'finance'}
]
const typeIndex = ref(0)
const statType = computed(() => statTypes[typeIndex.value])
const stat = computed(() => {
  if (statObject.value === null) return null
  return statObject.value[statType.value.value]
})

const tableRows = [
  {
    name: "Number of Rigs",
    unit: "number",
  },
  {
    name: "Energy - Rigs",
    unit: "energy",
  },
  { 
    name: "Energy - Infra",
    unit: "energy",
  }, 
  { 
    name: "Energy",
    unit: "energy",
  }, 
  {
    name: "Hash Rate",
    unit: "hashRate",
  }, 
  {
    name: "Hashes",
    unit: "hashes",
  }, 
  {
    name: "Hash Share",
    unit: "percentage",
  }, 
  {
    name: "BTC Reward",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  }, 
  {
    name: "Transaction Fees",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  }, 
  {
    name: "Pool Fees (Ƀ)",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  }, 
  {
    name: "BTC Mined",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  },
  // Income Statement
  {
    name: "BTC Converted for Expenses",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  },
  {
    name: "BTC Earned",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  },
  {
    name: "BTC, if held",
    unit: "BTC",
    formatArgs: {toFixed: 2},
  },
  // ROI
  {
    name: 'ROI, sold',
    unit: 'percentage',
    formatArgs: {toFixed: 2},
  },
  {
    name: 'ROI, held',
    unit: 'percentage',
    formatArgs: {toFixed: 2},
  }
]
const tableRowNames = tableRows.map((row) => row.name)
const rowFormat = (data, field) => {
  if (tableRowNames.includes(data.index)) {
    let row = tableRows.find(row => row.name === data.index)
    return format[row.unit](data[field], row.formatArgs)
  } else {
    return format.currency(data[field])
  }
}

const columns = computed(() => {
  let baseCols = [{
    field: 'index',
    header: 'Item',
    frozen: true,
    sortable: true,
    headerClass: 'table-header-left min-col-width-10',
    bodyClass: 'table-body-left min-col-width-10',
  }]
  let headerParams = {
    headerClass: 'table-header-center min-col-width-7dot5',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: rowFormat,
  }
  let table = new NewTableMaker({
    columns: baseCols, 
    otherHeaders: stat.value.columns.slice(1),
    headerParams
  })
  return table.columns
})
</script>
  
<template>
  <v-toolbar
    density="compact"
    color="surface"
    class="mt-0 pt-1 px-2"
  >
    <v-btn-toggle
      v-model="typeIndex"
      class="mr-6"
      mandatory
    >
      <v-btn
        v-for="statType in statTypes"
        :key="statType"
        :icon="'mdi-' + statType.icon"
      >
      </v-btn>
    </v-btn-toggle>
    <v-divider vertical class="mt-2"></v-divider>
    <v-btn-toggle
      v-model="freqIndex"
      class="vertical"
      mandatory
    >
      <v-btn 
        v-for="freq in statStore.allowedFreqs"
        :key="freq"
      >
        {{ freq }}
      </v-btn>
    </v-btn-toggle>
  </v-toolbar>
  <SimpleTable
    v-if="stat"
    :data="stat.stat"
    :columns="columns"
    :loading="statState?.isLoading"
    class="ma-3 pa-6 mb-0 pb-3"
  />
</template>
  
<style scoped>
  
</style>