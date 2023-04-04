<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'

import MainWindow from './projectSimulator/MainWindow.vue'
import BaseChart from '../components/reuseable/charts/BaseChart.vue'

import client from '@/services/client'
import { useFormatHelpers, useFormHelpers, TableMaker } from '@/services/composables'

import { 
  useRigStore,
  useRejectionStore, 
  useWeatherStationStore, 
  useWeatherDataStore,
  useCurrentStateStore,
} from '../stores/modules'
import ChartScroll from './reuseable/charts/ChartScroll.vue'
import SimpleTable from './reuseable/SimpleTable.vue'

const stationStore = useWeatherStationStore()
const dataStore = useWeatherDataStore()
const rejectionStore = useRejectionStore()
const rigStore = useRigStore()
const stateStore = useCurrentStateStore()
const format = useFormatHelpers()
const formHelpers = useFormHelpers()

const { numberRules } = storeToRefs(formHelpers)

const { objects } = storeToRefs(dataStore)

const view = ref(0)
const region = ref('Texas') // Regions are only brought over as the name, not objects; so no need to search thru index
const station = ref(null)
const stationIndex = ref(-1)

const stations = computed(() => {
  if (region.value)
    return stationStore.objects.filter((obj) => obj.region === region.value)
  else
    return []
})
const object = computed(() => {
  return objects.value[0]
})

watch(() => station.value, (newVal, oldVal) => {
  if (newVal) {
    let params = {
      station: station.value.id,
      variable: "Dry-Bulb",
      type: "Single-Variable Frequency",
      period: 'Annual',
    }
    dataStore.getObjects(params)
    stationIndex.value = stations.value.findIndex((obj) => obj.id === station.value.id)
  }
})
watch(() => stationIndex.value, (newVal, oldVal) => {
  if (newVal >= 0) {
    station.value = stations.value[newVal]
  }
})
const chartArgs = computed(() => {
  let labels = object.value?.data["Dry-Bulb °F"]
  let datasets = []
  datasets.push({
    label: 'Frequency hr',
    data: object.value?.data['Frequency hr'],
  })
  
  return {
    chartType: 'bar',
    labels, datasets, xLabel: 'Dry-Bulb °F', yLabel: 'Frequency hr',
    options: {plugins: {legend: {display: false}}}
  }
})

// Section covers form and output for the Dry Bulb Scaler
const { objects: rigs } = storeToRefs(rigStore)
const { objects: rejections } = storeToRefs(rejectionStore)

const rejection = ref(null)
const rejectionIndex = ref(0)
const rig = ref(null)
const capacity = ref(40000000)
const price = ref(0)
const reward = ref(0)
const difficulty = ref(0)
const tempImpact = ref(null)
const payback = ref(null)

const getRejectionTemperatureImpact = () => {
  client.getRejectionTemperatureImpact({
    station: station.value.id,
    rig: rig.value.id,
    rejection: rejection.value.id, 
    capacity: capacity.value,
    reward: reward.value,
    difficulty: difficulty.value,

  }).then((response) => {
    tempImpact.value = response.data
  })
  .catch((error) => {
    console.error(error.response)
  })
}
const getRejectionTemperaturePayback = () => {
  client.getRejectionTemperaturePayback({
    station: station.value.id,
    rig: rig.value.id,
    capacity: capacity.value,
    reward: reward.value,
    difficulty: difficulty.value,
    price: price.value,
  }).then((response) => {
    payback.value = response.data
  })
  .catch((error) => {
    console.error(error.response)
  })
}
const coolerColumns = computed(() => {
  let cols = [
  {
    field: 'Ambient Temp (F)',
    header: 'Ambient Temp (F)', 
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.temperature(data[field]),
  },
  {
    field: 'Capacity (W)',
    header: 'Capacity (W)',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.power(data[field]),
  },
  {
    field: 'Frequency hr',
    header: 'Frequency hr',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.number(data[field]),
  },
  {
    field: 'Frequency %',
    header: 'Frequency %',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.percentage(data[field] / 100),
  },
  {
    field: 'Cumulative Frequency %',
    header: 'Cumulative Frequency %',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.percentage(data[field] / 100),
  },
  {
    field: 'Hash Rate per Cooler',
    header: 'Hash Rate per Cooler',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.hashRate(data[field]),
  },
  {
    field: 'Number of Coolers',
    header: 'Number of Coolers',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.number(data[field]),
  },
  {
    field: 'Project Hash Rate',
    header: 'Project Hash Rate',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.hashRate(data[field]),
  },
  {
    field: 'Project Hashes per Block',
    header: 'Project Hashes per Block',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.hashes(data[field]),
  },
  {
    field: 'Win Share',
    header: 'Win Share',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.percentage(data[field]),
  },
  {
    field: 'Expected BTC Earned per Block',
    header: 'Expected BTC Earned per Block',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.BTC(data[field], {toFixed: 2}),
  },
  {
    field: 'Expected BTC Earned, Annual',
    header: 'Expected BTC Earned, Annual',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.BTC(data[field]),
  },
  {
    field: 'Weighted Expected BTC Earned, Annual',
    header: 'Weighted Expected BTC Earned, Annual',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.BTC(data[field]),
  },
  
]
  let table = new TableMaker(cols)
  return table.columns
})

const paybackColumns = computed(() => {
  let cols = [
  {
    field: 'design_dry_bulb',
    header: 'Ambient Temp (F)', 
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.temperature(data[field]),
  },
  {
    field: 'cost_of_coolers',
    header: 'Cost of Coolers',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.number(data[field]),
  },
  {
    field: 'incremental_cost',
    header: 'Incremental Cost',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.currency(data[field]),
  },
  {
    field: 'cumulative_cost',
    header: 'Cumulative Cost',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.currency(data[field]),
  },
  {
    field: 'expected_loss',
    header: 'Expected Loss',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: (data, field) => format.BTC(data[field], {toFixed: 2}),
  },
  {
    field: 'incremental_gain',
    header: 'Incremental Gain',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.BTC(data[field], {toFixed: 2}),
  },
  {
    field: 'cumulative_gain',
    header: 'Cumulative Gain',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.BTC(data[field], {toFixed: 2}),
  },
  {
    field: 'cumulative_gain_usd',
    header: 'Cumulative Gain',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.currency(data[field]),
  },
  {
    field: 'payback',
    header: 'Payback',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: (data, field) => format.number(data[field], {toFixed: 2}),
  }]
  let table = new TableMaker(cols)
  return table.columns
})

watch(() => [
    rejection.value, rig.value, price.value, capacity.value,
    reward.value, difficulty.value, station.value
  ], (newVal, oldVal) => {

  if (newVal && newVal.every((val) => val !== null && val !== undefined)) {
    rejectionIndex.value = rejections.value.findIndex((obj) => obj.id === rejection.value.id)
    getRejectionTemperatureImpact()
    getRejectionTemperaturePayback()
  }
})
watch(() => rejectionIndex.value, (newVal, oldVal) => {
  if (newVal >= 0) {
    rejection.value = rejections.value[newVal]
  }
})

// This code requires (at least right now), that the station data and the cooler data are handled
// in the same component, b/c we must wait for station to be grabbed before we can get the cooler data
onMounted(() => {
  price.value = stateStore.objects.Price
  reward.value = stateStore.objects.Reward
  difficulty.value = stateStore.objects.Difficulty

  stationStore.getObjects().then(() => {
    let initIndex = stationStore.objects.findIndex((obj) => obj.location === 'Abilene')    
    station.value = stationStore.objects[initIndex]
    dataStore.getObjects({station: station.value.id})

    // Now can trigger the cooler data
    rejection.value = rejections.value[rejectionIndex.value]
    rig.value = rigs.value[0]
  })
})
</script>

<template>
  <MainWindow>
    <template #nav-panel>
      <v-combobox
        v-model="region"
        :items="stationStore.regions"
        label="Region"
        outlined
        dense
        class="mt-0 pl-3 pr-3"
      />
      <v-combobox
        v-model="station"
        :items="stations"
        item-title="location"
        item-value="id"
        label="Weather Station"
        outlined
        dense
        class="mt-0 pl-3 pr-3"
      />
      <v-combobox
        v-model="rejection"
        :items="rejections"
        label="Heat Rejection"
        item-title="name"
        item-value="id"
        class="mt-0 pl-3 pr-3"
        required
      />
      <v-combobox
        v-model="rig"
        :items="rigs"
        label="Rig name"
        item-title="name"
        item-value="id"
        class="mt-0 pl-3 pr-3"
        required
      />
      <v-sheet class="d-flex justify-space-between mt-0 pl-3 pr-3">
        <v-text-field
          @update:model-value="(val) => capacity = val*1000000"
          :model-value="capacity/1000000"
          :rules="numberRules"
          label="Project Size"
          suffix="MW"
          outlined
          dense
          class="mr-2"
        />
        <v-text-field
          v-model.number="price"
          :rules="numberRules"
          label="Price"
          prefix="$"
          outlined
          dense
          class="ml-2"
        />
      </v-sheet>
      <v-sheet 
        class="d-flex justify-space-between mt-0 pl-3 pr-3"
      >
        <v-text-field
          v-model.number="reward"
          :rules="numberRules"
          label="Reward"
          :prefix="format.btcStr"
          outlined
          dense
          class="mr-2"
        />
        <v-text-field
          @update:model-value="(val) => difficulty = val*1e12"
          :model-value="(difficulty/1e12).toFixed(2)"
          :rules="numberRules"
          label="Difficulty"
          suffix="T"
          outlined
          dense
          class="ml-2"
        />
      </v-sheet>
    </template>
    <template #main-panel>
      <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
        <v-toolbar 
          density="compact"
          color="surface"
          class="pt-2"
        >
          <v-btn-toggle
            v-model="view"
            class="mr-6"
            mandatory
          >
            <v-btn>
              Dry Bulb Frequency
            </v-btn>
            <v-btn>
              Dry Bulb Impact
            </v-btn>
            <v-btn>
              Cooler Payback
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
        <ChartScroll
          v-if="view === 0 && station && object"
          :num-objects="stations?.length"
          v-model:objects-index="stationIndex"
        >
          <template #chart>
            <BaseChart v-bind="chartArgs"></BaseChart>
          </template>
        </ChartScroll>
        <ChartScroll
          v-if="view === 1 && rejection && rig"
          :num-objects="rejections?.length"
          v-model:objects-index="rejectionIndex"
          scroll-position="top"
        >
          <template #chart>
            <v-row>
              <v-col>
                <span class="text-body-2 text-medium-emphasis mr-3">Expected Annual Loss:</span>
                {{ format.BTC(tempImpact.expected_loss, {toFixed: 2}) }}
              </v-col>
            </v-row>
            <SimpleTable
              :columns="coolerColumns"
              :data="tempImpact?.data"
            />
          </template>
        </ChartScroll>
        <ChartScroll 
          v-if="view === 2 && payback"
          :num-objects="stations?.length"
          v-model:objects-index="stationIndex"
          scroll-position="bottom"
        >
          <template #chart>

            <SimpleTable
              :columns="paybackColumns"
              :data="payback"
            />
          </template>
        </ChartScroll>
      </v-container>
    </template>
  </MainWindow>
    
</template>

<style scoped>
  
</style>

