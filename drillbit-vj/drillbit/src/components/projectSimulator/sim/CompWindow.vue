<script setup>
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState } from '@vueuse/core'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import BaseChart from '@/components/reuseable/charts/BaseChart.vue'
import PlaceholderChart from '../../reuseable/charts/PlaceholderChart.vue'
import ChartScroll from '../../reuseable/charts/ChartScroll.vue'

import { useEnvironmentStore, useProjectsStore, useStatementStore } from '@/stores/modules'

import { useFormatHelpers, TableMaker } from '@/services/composables'

const envStore = useEnvironmentStore()
const projectsStore = useProjectsStore()
const statStore = useStatementStore()
const formatHelpers = useFormatHelpers()
const view = ref(1)
const tableType = ref(0)

const { allTasksComplete } = storeToRefs(statStore)

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
const freq = ref(2)
const freqState = ref(null)

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
const chartItems = computed(() => [
  {
    title: 'Environment',
    type: 'header'
  },
  {
    title: 'Hashes',
    type: 'subheader'
  },
  {   
    title: 'Number of Rigs',
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
    title: 'Energy Consumption',
    type: 'subheader'
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
    title: 'Rewards',
    type: 'subheader'
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
  {
    type: 'divider'
  },
  {
    title: 'Financials',
    type: 'header'
  },
  {
    title: 'Income Statement',
    type: 'subheader'
  },
  ...istat_dollar_accounts.map((account) => {
    return {
      title: account,
      yTickFormat: 'currency',
    }
  }),
  {
    title: 'Bitcoin',
    type: 'subheader'
  },
  ...istat_bitcoin_accounts.map((account) => {
    return {
      title: account,
      yTickFormat: 'BTC',
    }
  }),
  {
    title: 'ROI',
    type: 'subheader'
  },
  ...roi_dollar_accounts.map((account) => {
    let yTickFormat = ['ROI, sold', 'ROI, held'].includes(account) ? 'percentage' : 'currency'
    return {
      title: account,
      yTickFormat,
      disabled: freq.value < 2
    }
  })
])

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
          display: true,
          position: 'bottom',
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
    yTickFormat: chartItems.value.find((item) => item.title === accounts.value[accountIndex.value]).yTickFormat,
  }
}

watch(() => allTasksComplete.value, (allTasksComplete) => {
  if (allTasksComplete) {
    var params = {
      environment: envStore.object.id,
      projects: projectsStore.object.projects.map((project) => project.id),
      frequency: 'M',
    }
    freqState.value = useAsyncState(
      statStore.getByAccount({params}).then(() => {
        updateChartArgs()
      }),
      {},
      {
        onError: (error) => {
          console.error(error.response ?? error)
        }
      }
    )
  }
})
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
watch(() => freq.value, (newVal) => {
  var params = {
    environment: envStore.object.id,
    projects: projectsStore.object.projects.map((project) => project.id),
    frequency: statStore.allowedFreqs[newVal],
  }
  freqState.value = useAsyncState(
    statStore.getByAccount({params}).then(() => {
      updateChartArgs()
    }),
    {},
    {
      onError: (error) => {
        console.error(error.response ?? error)
      }
    }
  )
})

</script>

<template>
  <v-toolbar
    density="compact"
    color="surface"
    class="mt-0 pt-1 px-2"
  >
    <v-btn-toggle
      v-model="view"
      class="mr-6"
      mandatory
    >
      <v-btn
        icon="mdi-table"
        :disabled="!statStore.summary"
      />
      <v-btn
        icon="mdi-chart-bar"
        :disabled="!statStore.byAccount"
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
      :disabled="!statStore.byAccount"
      single-line
      multiple
      clearable
      chips
    >
      <template v-slot:item="{ item, props }">
        <v-divider v-if="item.raw.type === 'divider'" />
        <v-card-title 
          v-else-if="item.raw.type === 'header'"
          class="font-weight-medium text-medium-emphasis">
          {{ item.title }}
        </v-card-title>
        <v-list-subheader v-else-if="item.raw.type === 'subheader'">
          {{ item.title }}
        </v-list-subheader>
        <v-list-item 
          v-else 
          v-bind="props" 
          class="ml-3"
          :disabled="item.raw.disabled"
        />
      </template>
    </v-select>
  </v-toolbar>
  <SimpleTable
    v-if="view === 0 && data?.length > 0"
    :data="data"
    :columns="columns"
    class="ma-3 pa-6 mb-0 pb-3"
  />
  <v-card
    v-else-if="view === 1"
    class="mb-0 pb-0"
    flat
  >

      <PlaceholderChart 
        v-if="accounts.length === 0 || !chartArgs"
        :min-height="600"
        class="mt-12"
      />
      <div 
        v-else-if="chartArgs"
      >
        <v-row class="mt-3">
          <v-col cols="1" 
            class="d-flex align-center justify-center flex-column mt-8 mr-0 pr-0"
          >
            <v-progress-circular
              v-if="freqState?.isLoading"
              color="secondary"
              :size="20"
              indeterminate
            />
            <div
              v-else
              class="mt-5"
            ></div>
            <v-btn-toggle
              v-model="freq"
              class="vertical"
              mandatory
            >
              <div v-for="freq in statStore.allowedFreqs"
                :key="freq"
              >
                <v-btn 
                  size="small"
                >
                {{ freq }}
                </v-btn>
              </div>
            </v-btn-toggle>
          </v-col>
          <v-col class="ml-0 pl-0">
            <ChartScroll
              :num-objects="accounts?.length"
              v-model:objects-index="accountIndex"
            >
              <template #chart>
                <span class="text-caption font-italic">*Values are monthly aggregates</span>
                <BaseChart v-bind="chartArgs"/>
              </template>
            </ChartScroll>
          </v-col>
        </v-row>
      </div>
  </v-card>
</template>
  
<style scoped>
:deep(.v-btn-toggle.vertical) {
  flex-direction: column;
  height: 100%;
}
</style>

