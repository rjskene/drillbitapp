<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import BaseChart from '@/components/reuseable/charts/BaseChart.vue'
import PlaceholderChart from '../../reuseable/charts/PlaceholderChart.vue'
import ChartScroll from '../../reuseable/charts/ChartScroll.vue'

import { useProjectsStore, useStatementStore } from '@/stores/modules'

import { useFormatHelpers, TableMaker } from '@/services/composables'

const projectsStore = useProjectsStore()
const statStore = useStatementStore()
const formatHelpers = useFormatHelpers()
const view = ref(1)
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
        bodyFunc: rowFormat,
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

/* Charts Section */
const accounts = ref([])
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

/* 
Chart Args Section

Handles the chartArgs reactive object that is passed to the chart component. 

updateChartArgs pulls data from the statStore and formats it for the chart component. The function
is called when 

1) the accounts reactive object is updated, which happens when the user selects a new
account from the dropdown menu.
2) when the next or previous button is clicked, which changes the accountIndex reactive object.
*/
const chartArgs = ref(null)
const updateChartArgs = () => {
  let labels = statStore.byAccount?.labels
  let datasets = statStore.byAccount?.datasets[accounts.value[accountIndex.value]]

  chartArgs.value = {
    labels,
    datasets,
    title: accounts.value[accountIndex.value],
    options: {
      plugins: {
        legend: {
          display: false,
        },
      },
    },
    xScaleOptions: {
      type: 'time',
      time: {
        unit: 'quarter',
        displayFormats: {
          quarter: 'MMM YYYY'
        },
      }
    },
    // yTickFormat: activeElement.value?.chartOptions.yTickFormat,
    // yTickFormatOptions: activeElement.value?.chartOptions.yTickFormatOptions,
  }
}
watch(() => accounts.value, (newVal) => {
  if (newVal.length > 0) {
    accountIndex.value = accounts.value.length - 1
    updateChartArgs()
  } else {
    chartArgs.value = null
  }
})
watch(() => accountIndex.value, (newVal) => {
  updateChartArgs()
})

</script>

<template>
  <v-container>
  <v-row class="h-100">
    <v-col class="h-100">
      <v-toolbar
        density="compact"
        color="surface"
        class="pt-2 px-2"
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
          single-line
          multiple
          clearable
          chips
        />
      </v-toolbar>
      <SimpleTable
        v-if="view === 0 && data?.length > 0"
        :data="data"
        :columns="columns"
        class="ma-3 pa-6 mb-0 pb-3"
      />
      <v-card
        v-else-if="view === 1 && statStore.byAccount"
        class="ma-3 pa-6 mb-0 pb-0"
        flat
      >
          <PlaceholderChart 
            v-if="accounts.length === 0 || !chartArgs"
            min-height="600"
          />
          <ChartScroll
            v-else-if="chartArgs"
            :num-objects="accounts?.length"
            v-model:objects-index="accountIndex"
          >
            <template #chart>
              <span class="text-caption font-italic">*Values are monthly aggregates</span>
              <BaseChart v-bind="chartArgs"/>
            </template>
          </ChartScroll>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>
  
<style scoped>
</style>

