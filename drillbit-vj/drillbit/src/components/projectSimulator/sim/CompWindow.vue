<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import MultiLineChart from '@/components/reuseable/MultiLineChart.vue'

import { useProjectsStore, useStatementStore } from '@/stores/modules'

import { useFormHelpers, useFormatHelpers, TableMaker } from '@/services/composables'

const projectsStore = useProjectsStore()
const statStore = useStatementStore()
const formHelpers = useFormHelpers()
const formatHelpers = useFormatHelpers()
const view = ref(0)
const tableType = ref(0)

const columns = computed(() => {
  let cols = [
    {
      field: 'index',
      header: '', 
      headerClass: 'table-header-left',
      bodyClass: 'table-body-left min-col-width-7dot5',
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
        bodyFuncWithDataAccess: rowFormat,
      })
    })

  let table = new TableMaker(cols)
  return table.columns
})

const summary_dollar_rows = [
  'Rig Costs', 'Total Infra Costs', 'Capital Costs', 'Total Cost',
  'Net Cash Flow, held',
  'Net Gain, held'
]
const summary_hash_price_rows = [
  'Rigs Hash Price', 'Infra Hash Price', 'Build Hash Price', 'Cash Hash Price'
]
const summary_percent_rows = [
  'ROI, held', 'IRR 3-year, held', 'IRR 5-year, held', 'IRR terminal, held'
]

const tableRows = computed(() => {
  let tableRows = [
    {
      name: 'Capacity', 
      unit: 'power',
    }, 
    {
      name: 'Compute Power',
      unit: 'power',
    },
    {
      name: 'Infra Power',
      unit: 'power',
    },
    {
      name: 'Number of Rigs',
      unit: 'number',
    },
    {
      name: 'HR / rig',
      unit: 'hashRate',
    },
    {
      name: 'Hash Rate',
      unit: 'hashRate',
    },
    {
      name: 'Total Hashes',
      unit: 'hashes',
    },
    {
      name: 'Energy Consumption',
      unit: 'energy',
    },
    {
      name: 'Efficiency',
      unit: 'efficiency',
    },
    ...summary_dollar_rows.map((row) => {
      return {
        name: row,
        unit: 'currency',
      }
    }),
    ...summary_hash_price_rows.map((row) => {
      return {
        name: row,
        unit: 'hashPrice',
      }
    }),
    ...summary_percent_rows.map((row) => {
      return {
        name: row,
        unit: 'percentage',
      }
    }),
    {
      name: 'BTC, held',
      unit: 'BTC',
    }
  ]
  return tableRows
})
const tableRowsByName = computed(() => {
  let tableRowsByName = {}
  tableRows.value.forEach((row) => {
    tableRowsByName[row.name] = row
  })
  return tableRowsByName
})

const rowFormat = (data, field) => {
  if (Object.keys(tableRowsByName.value).includes(data.index)) {
    let unit = tableRowsByName.value[data.index].unit
    return formatHelpers[unit](data[field])
  } else {
    return data[field]
  }
}

const rows = computed(() => {
  let tableRows = [
    [
      'Capacity', 'Compute Power', 'Infra Power', 
      'Number of Rigs', 'HR / rig',
      'Hash Rate',
      'Total Hashes', 'Energy Consumption', 'Efficiency'
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
const chartWindow = ref(0)
const accountIndex = ref(0)
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
const chartItems = [
  // {
  //   header: 'Environment',
  //   disabled: true,
  // },
  {   
    title: 'Number of Miners',
    yTickFormat: 'number',
  },
  {
    title: 'Hash Rate',
    yTickFormat: 'hashRate'
  },
  {
    title: 'Hashes',
    yTickFormat: 'hashes',
  },
  {
    title: 'Hash Share',
    yTickFormat: 'percentage',
  },
  {
    title: 'Energy - Miner',
    yTickFormat: 'energy',
  },
  {
    title: 'Energy - Infra',
    yTickFormat: 'energy',
  },
  {
    title: 'Energy',
    yTickFormat: 'energy',
  },
  {
    title: 'BTC Reward',
    yTickFormat: 'BTC',
  },
  {
    title: 'Transaction Fees',
    yTickFormat: 'BTC',
  },
  {
    title: 'Pool Fees (\u0243)',
    yTickFormat: 'BTC',
  },
  {
    title: 'BTC Mined',
    yTickFormat: 'BTC',
    description: 'BTC Mined = BTC Reward + Transaction Fees - Pool Fees',
  },
  // {
  //   title: 'Income Statement',
  //   value: 'Income Statement',
  //   header: true,    
  // },
  ...istat_dollar_accounts.map((account) => {
    return {
      title: account,
      yTickFormat: 'currency',
    }
  }),
  ...istat_bitcoin_accounts.map((account) => {
    return {
      title: account,
      yTickFormat: 'BTC',
    }
  }),
  // {
  //   title: 'ROI',
  //   header: true,
  // },
  ...roi_dollar_accounts.map((account) => {
    return {
      title: account,
      yTickFormat: 'currency',
    }
  })
]
const chartItemsObject = computed(() => {
  let obj = {}
  chartItems.forEach((item) => {
    obj[item.title] = item
  })
  return obj
})
const next = () => {
  accountIndex.value = accountIndex.value >= accounts.value.length - 1 ? 0 : accountIndex.value + 1
}
const prev = () => {
  accountIndex.value = accountIndex.value <= 0 ? accounts.value.length - 1 : accountIndex.value - 1
}
</script>

<template>
  <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
    <v-toolbar 
      density="compact"
      color="surface"
      class="pt-2"
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
          :disabled="!statStore.summary"
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
        :items="chartItems"
        multiple
        clearable
        chips
      />

    </v-toolbar>
    <SimpleTable
      v-if="view === 0 && data?.length > 0"
      :data="data"
      :columns="columns"
      class="ma-3 pa-6 mb-0 pb-0"
    />
    <v-card
      v-else-if="view === 1 && statStore.byAccount && accounts.length > 0"
      elevation="0"
      class="ma-3 pa-6 mb-0 pb-0"
    >
      <span class="text-caption font-italic">*Values are monthly aggregates</span>
      <MultiLineChart
        :labels="statStore.byAccount?.labels"
        :datasets="statStore.byAccount?.datasets[accounts[accountIndex]]"
        v-bind="chartItemsObject[accounts[accountIndex]]"
      />
      <v-card-actions class="justify-space-between">
        <v-btn
          variant="plain"
          icon="mdi-chevron-left"
          @click="prev"
        ></v-btn>
        <v-item-group
          v-model="accountIndex"
          class="text-center"
          mandatory
        >
          <v-item
            v-for="n in accounts.length"
            :key="`btn-${n - 1}`"
            v-slot="{ isSelected, toggle }"
            :value="n - 1"
          >
            <v-btn
              :variant="isSelected ? 'outlined' : 'text'"
              icon="mdi-record"
              @click="toggle"
            ></v-btn>
          </v-item>
        </v-item-group>
        <v-btn
          variant="plain"
          icon="mdi-chevron-right"
          @click="next"
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
  
<style scoped>
</style>

