<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import MultiLineChart from '@/components/reuseable/MultiLineChart.vue'

import { useProjectsStore, useStatementStore } from '@/stores/modules'

import { useFormHelpers, TableMaker } from '@/services/composables'

const projectsStore = useProjectsStore()
const statStore = useStatementStore()
const formHelpers = useFormHelpers()
const view = ref(0)
const tableType = ref(0)

const columns = computed(() => {
  let cols = [
    {
      field: 'index',
      header: '', 
      headerClass: 'table-header-center',
      bodyClass: 'table-body-center min-col-width-7dot5',
    }
  ]
  if (projectsStore.object?.projects?.length === 0) return []
  else
    projectsStore.object?.projects?.forEach((project) => {
      cols.push({
        field: project.name,
        header: project.name, 
        headerClass: 'table-header-center',
        bodyClass: 'table-body-center min-col-width-7dot5',
      })
    })

  let table = new TableMaker(cols)
  return table.columns
})

const rows = computed(() => {
  let tableRows = [
    [
      'Capacity', 'Compute Power', 'Infra Power', '# of Rigs', 'HR / rig',
      'Hash Rate',
      'Total Hashes', 'Energy Use', 'Efficiency'
    ],
    ['Rig Costs', 'Total Infra Costs', 'Capital Costs', 'Total Cost'],
    ['Rigs Hash Price', 'Infra Hash Price', 'Build Hash Price', 'Cash Hash Price'],
    [
      'BTC, held', 'Net Cash Flow, held', 
      'Net Gain, held', 'ROI, held', 
      'IRR 3-year, held', 'IRR 5-year, held', 'IRR terminal, held', 'Breakeven'
    ]
  ]
  return tableRows[tableType.value]
})
const data = computed(() => {
  return statStore.summary?.filter((obj) => rows.value.includes(obj.index))
})

const accounts = ref([])
const chartSelectItems = computed(() => {
  if (statStore.byAccount?.datasets)
    return Object.keys(statStore.byAccount?.datasets)
  else
    return null
})
let istat_dollar_accounts = [
  'Revenue - Reward', 'Revenue - Fees', 'Gross Revenue', 'Pool Fees',
  'Net Revenue', 'Energy Expenses', 'Gross Profit', 'Gross Margin',
  'Operating Expenses', 'Property Tax', 'EBITDA', 'Rig Amortization',
  'Infra Amortization', 'Depreciation for Taxes', 'EBIT', 'Taxes',
  'Profit, if sold', 'Operating Cash Flow, if sold', 'Cash Expenses',
  'BTC Value, if held'
]
let istat_bitcoin_accounts = ['BTC Converted for Expenses', 'BTC Earned', 'BTC, if held']
let roi_dollar_accounts = [
  'Rigs Outlay', 'Infrastructure Outlay', 'Building Outlay',
  'Cash Outlays', 'Operating Cash Flow, held', 'Operating Cash Flow, sold',
  'Net Cash Flow, sold', 'Net Cash Flow, held',
  'Cumulative Net, sold', 'Cumulative Net, held',
  'ROI, sold', 'ROI, held'
]
const items = [
  {
    divider: true,
  },
  {   
    title: 'Number of Miners',
    value: 'Number of Miners',
    unit: '#'
  },
  {
    title: 'Energy - Miner',
    value: 'Energy - Miner',
    unit: 'kWh'
  },
  {
    title: 'Energy - Infra',
    value: 'Energy - Infra',
    unit: 'kWh'
  },
  {
    title: 'Energy',
    value: 'Energy',
    unit: 'kWh'
  },
  {
    title: 'Hash Rate',
    value: 'Hash Rate',
    unit: 'TH/s'
  },
  {
    title: 'Hashes',
    value: 'Hashes',
    unit: 'TH'
  },
  {
    title: 'Hash Share',
    value: 'Hash Share',
    unit: '%'
  },
  {
    title: 'BTC Reward',
    value: 'BTC Reward',
    unit: 'BTC'
  },
  {
    title: 'Transaction Fees',
    value: 'Transaction Fees',
    unit: 'BTC'
  },
  {
    title: 'Pool Fees (\u0243)',
    value: 'Pool Fees (\u0243)',
    unit: 'BTC'
  },
  {
    title: 'BTC Mined',
    value: 'BTC Mined',
    unit: 'BTC',
    description: 'BTC Mined = BTC Reward + Transaction Fees - Pool Fees'
  },
  {
    title: 'Income Statement',
    value: 'Income Statement',
    header: true,    
  },
  ...istat_dollar_accounts.map((account) => {
    return {
      title: account,
      value: account,
      unit: '$'
    }
  }),
  ...istat_bitcoin_accounts.map((account) => {
    return {
      title: account,
      value: account,
      unit: 'BTC'
    }
  }),
  {
    title: 'ROI',
    value: 'ROI',
    header: true,    
  },
  ...roi_dollar_accounts.map((account) => {
    return {
      title: account,
      value: account,
      unit: '$'
    }
  })
]
console.log(items)
</script>

<template>
  <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
    <v-toolbar 
      density="compact"
      color="surface"
      class="pt-6"
    >
      <v-btn-toggle
        v-model="view"
        :disabled="!statStore.summary"
        class="mr-6"
        mandatory
      >
        <v-btn
          icon="mdi-table"
        />
        <v-btn
          icon="mdi-chart-bar"
        />
      </v-btn-toggle>
      <v-divider vertical class="mt-2"></v-divider>
      <v-btn-toggle
        v-if="view === 0"
        v-model="tableType"
        :disabled="!statStore.summary"
        class="ml-6"
        mandatory
      >
        <v-btn icon="mdi-scale-balance"/>
        <v-btn icon="mdi-currency-usd"/>
        <v-btn icon="mdi-pound"/>
        <v-btn icon="mdi-chart-line-variant"/>
      </v-btn-toggle>
      <v-select
        v-else
        v-model="accounts"
        label="Select accounts"
        class="mt-6 ml-6"
        :items="items"
        multiple
        clearable
        chips
      />

    </v-toolbar>
    <SimpleTable
      v-if="view === 0 && data?.length > 0"
      :data="data"
      :columns="columns"
    />
    <v-container 
      v-else-if="view === 1 && statStore.byAccount && accounts.length > 0"
      class="ma-3 d-flex justify-space-around flex-wrap"
    >
 
        <MultiLineChart
          v-for="account in accounts"
          :labels="statStore.byAccount?.labels"
          :datasets="statStore.byAccount?.datasets[account]"
          :title="account"
        />
    </v-container>
  </v-container>
</template>
  
<style scoped>
</style>

