<!-- PROJECT FORM -->
<!--

  This is the main form for creating and editing projects.

  The form is only passed the id of the project (no other data!). 
  The form then fetches all other data from the store.

 -->
<script setup>

import { ref, toRefs, computed, onMounted, watch, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState, useRefHistory } from '@vueuse/core'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import ChartScroll from '../../reuseable/charts/ChartScroll.vue'
import BaseChart from '../../reuseable/charts/BaseChart.vue'
import ProjectFormInfraSection from './ProjectFormInfraSection.vue'
import ProjectFormRigSection from './ProjectFormRigSection.vue'

import { 
  useProjectStore,
  useRigStore, 
  useWeatherStationStore, 
  useWeatherDataStore,
} from '@/stores/modules'

import { useFormHelpers } from '@/services/composables'

const { nameRules, numberRules, percentageRules } = useFormHelpers()
const store = useProjectStore()
const stationStore = useWeatherStationStore()
const dataStore = useWeatherDataStore()
const rigStore = useRigStore()

const props = defineProps({
  project: {
    type: Object,
    default: null
  }
})

const { project } = toRefs(props)
const emit = defineEmits(['close'])
const changesNotSaved = ref(false)

const update = async () => {
  await store.updateObject({
      pk: project.value.id,
      params: project.value,
  }).then(() => {
    store.getObjects()
    changesNotSaved.value = false
  })
}
const { history, undo, redo } = useRefHistory(project, {deep: true})
watch(history, (oldVal, newVal) => {
  if (JSON.stringify(oldVal) !== JSON.stringify(newVal))
    changesNotSaved.value = true
})

const projectStructure = computed(() => {
  return {
    '__auto_scale__': {
      default: false
    },
    name: {
      label: 'Name',
      density: 'compact',
      rules: nameRules.value,
      required: true,
      clearable: true,
      default: `Project ${store.projects.length + 1}`
    }, 
    description: {
      label: 'Description',
      density: 'compact',
      clearable: true,
    }, 
    capacity: {
      label: 'Power Capacity',
      suffix: 'MW',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 40000000,
    }, 
    energy_price: {
      label: 'Energy Price',
      suffix: '$/kWh',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 0.00005,
    }, 
    'target_overclocking': {
      label: 'Overclocking',
      suffix: 'x',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 1,
    }, 
    'ambient_temp_source_name': {
      label: 'Ambient Temperature Source Name',
    },
    'ambient_temp_source': {
      label: 'Ambient Temperature Source',
    },
    'target_ambient_temp': {
      label: 'Temperature',
      suffix: '°F',
      density: 'compact',
      required: false,
      rules: numberRules.value,
    },
    'pool_fees': {
      label: 'Pool Fees',
      suffix: '%',
      density: 'compact',
      required: true,
      rules: percentageRules.value,
      default: 0.025,
    },
    'tax_rate': {
      label: 'Tax Rate',
      suffix: '%',
      density: 'compact',
      required: true,
      rules: percentageRules.value,
      default: 0,
    },
    rigs: {
      label: 'Rigs',
      density: 'compact',
      items: rigStore.objects,
      itemTitle: 'name',
      itemValue: 'id',
      default: [{rig_id: null, price: null, quantity: null}],
      required: true,
    },
    infrastructure: {
      label: 'Infrastructure',
      required: true,
      default: [{infra_content_type: 'cooling', infra_object_id: null, price: null, quantity: null}]
    },
    buildingSize: {
      label: 'Size in Square Feet',
      density: 'compact',
      suffix: 'sf',
      rules: numberRules.value,
      default: 0,
    },
    buildingCost: {
      label: 'Cost per Square Foot',
      suffix: '$/sf',
      density: 'compact',
      rules: numberRules.value,
      default: 0,
    },
    opex: {
      label: 'Operating Expense',
      prefix: '$',
      density: 'compact',
      rules: numberRules.value,
      default: 0,
    }, 
    taxRate: {
      label: 'Tax Rate',
      density: 'compact',
      rules: numberRules.value,
      default: 0,
  }}
})

/* 
Manages state of the Temperature module

tempPanel = null; no panel is open
tempPanel = 0; the temperature panel is open

when the tempPanel is opened, the station and stationIndex are set
and the values for project.ambient_temp_source and project.target_ambient_temp are set

when the tempPanel is closed, the values for project.ambient_temp_source and project.target_ambient_temp are set to null

when a new object is passed to props.project, check to see if the project has a target_ambient_temp
if it does, open the temperature panel (tempPanel = 0). if the project has an ambient_temp_source, 
set the station to that source. this will fire the watch on station, which will set the stationIndex

to handle updates to the temperature panel via the chartScroll, the watchEffect on the tempPanel
and station will capture changes to the station, and in turn fetch the required visual data (via updateChartArgs)
and set the project.ambient_temp_source and project.target_ambient_temp

*/
const { objects: dataObjects } = storeToRefs(dataStore)
const dataObject = computed(() => {
  return dataObjects.value[0]
})

const tempPanel = ref(null) 
const region = ref('Texas') // Regions are only brought over as the name, not objects; so no need to search thru index
const loadState = ref(null)
const station = ref(null)
const stationIndex = ref(-1)

const stations = computed(() => {
  if (region.value) {
    return stationStore.objects.filter((obj) => obj.region === region.value)}
  else
    return []
})
watch(() => project.value, (newVal, oldVal) => {
  if (newVal) {
    if (newVal.target_ambient_temp)
      tempPanel.value = 0
    else
      tempPanel.value = null
  }
})
watch(() => tempPanel.value, (newVal, oldVal) => {
  if (newVal === 0) {
    stationStore.getObjects().then(() => {
      let location = project.value.ambient_temp_source_name ? project.value.ambient_temp_source_name : 'Abilene'
      let initIndex = stationStore.objects.findIndex((obj) => obj.location === location)    
      station.value = stationStore.objects[initIndex]
    })
} else if (!newVal) {
    project.value.ambient_temp_source = null
    project.value.target_ambient_temp = null
  }
})
watch(() => stations.value, (newVal, oldVal) => {
  if (newVal.length > 0) {
    station.value = stations.value[0]
  }
})
watch(() => station.value, (newVal, oldVal) => {
  if (newVal) {
    stationIndex.value = stations.value.findIndex((obj) => obj.id === station.value.id)
  }
})
watch(() => stationIndex.value, (newVal, oldVal) => {
  if (newVal >= 0) {
    station.value = stations.value[newVal]
  }
})

const updateTempParams = (stationId) => {
  if (stationId) {
    project.value.ambient_temp_source = station.value.id
    let obj = {}
    dataObject.value.periods.forEach((period, index) => {
      obj[period] = dataObject.value.data[index]
    })
    project.value.target_ambient_temp = obj
  }
}
watchEffect(() => {
  /* 
  Watch to add temperature data to project object
  The temp module must be selected, temp.value = true, and a station must be selected
  Then the data is loaded from the dataStore and added to the project object
  Chart args can be updated when the getObjects is completed as well
  */
  if (tempPanel.value == 0 && station.value) {
    let params = {
        station: station.value.id,
        variable: 'Dry-Bulb',
        type: 'Simulation',
        period: 'Annual',
      }
    loadState.value = useAsyncState(dataStore.getObjects(params))
    loadState.value.execute().then(() => {
      updateChartArgs()
      updateTempParams(station.value.id)
    })
  } 
})

const chartArgs = ref(null)
const updateChartArgs = () => {
  var labels = []
  var datasets = []
  labels = dataObject.value?.periods
  datasets.push({
    label: 'Dry-Bulb °F',
    data: dataObject.value?.data,
  })
  chartArgs.value = {
    chartType: 'scatter', 
    labels, 
    datasets,
    xScaleOptions: {
      type: 'time',
      time: {
        unit: 'quarter',
        displayFormats: {
          quarter: 'MMM YYYY'
        },
      }
    }
  }
}

// Equipment
const rig = computed(() => {
  return rigStore.findObjectById(project.value.rig)
})
const addRigs = () => {
  project.value.rigs.push({rig_id: null, price: null, quantity: null})
}
const updateRigId = (index, id) => {
  project.value.rigs[index].rig_id = id
}
const deleteRig = (index, pk) => {
  project.value.rigs.splice(index, 1)
}
const addInfrastructure = () => {
  project.value.infrastructure.push({infra_content_type: 'cooling', infra_object_id: null, price: null, quantity: null})
}
const updateInfraType = (index, type) => {
  project.value.infrastructure[index].infra_content_type = type
  project.value.infrastructure[index].infra_object_id = null
}
const updateInfraObjectId = (index, id) => {
  project.value.infrastructure[index].infra_object_id = id
}
const deleteInfra = (index, pk) => {
  project.value.infrastructure.splice(index, 1)
}
</script>
  
<template>
  <v-form>
    <v-card-title class="pb-0 mb-0">
      <v-text-field
        v-bind="projectStructure.name"
        v-model="project.name"
        :label="null"
        variant="outlined"
        density="comfortable"
      />
    </v-card-title>
    <v-sheet class="d-flex justify-left align-center mt-0 pt-0">
      <v-tooltip text="Tooltip" location="top" open-on-click>
        <template v-slot:activator="{ props }">
          <StatefulBtn
            @click="update"
            variant="flat"
            :icon="changesNotSaved ? 'mdi-alert': 'mdi-content-save'"
            :iconProps="changesNotSaved ? {color: 'red'} : {color: 'on-secondary'}"
          />
        </template>
      </v-tooltip>
      <v-checkbox
        v-model="project.__auto_scale__"
        label="Auto-scale"
        class="mt-6"
      />
    </v-sheet>
    <v-sheet
      class="d-flex justify-left mx-3"
    >
      <v-text-field
        v-bind="projectStructure.description"
        v-model="project.description"
      />
    </v-sheet>
    <v-divider></v-divider>
    <v-card-subtitle class="my-3">Specs</v-card-subtitle>
    <v-sheet
      class="d-flex justify-space-around mx-3"
    >
      <v-sheet
        min-width="200"
      >
        <v-text-field 
          v-bind="projectStructure.capacity" 
          @update:model-value="(val) => project.capacity = val*1000000"
          :model-value="project.capacity/1000000"
        />
        <v-text-field 
          v-bind="projectStructure.energy_price" 
          @update:model-value="(val) => project.energy_price = val/1000"
          :model-value="project.energy_price*1000"
        />
      </v-sheet>
      <v-sheet
        class="d-flex flex-column justify-space-between"
        min-width="200"
      >
        <v-text-field 
          v-bind="projectStructure.target_overclocking" 
          v-model="project.target_overclocking"
        />
        <v-text-field 
          v-bind="projectStructure.target_ambient_temp"
          v-model="project.target_ambient_temp"
          :disabled="true"
        />
      </v-sheet>
      <v-sheet
        class="d-flex flex-column justify-space-around"
        min-width="200"
      >
      <v-text-field
        v-bind="projectStructure.pool_fees"
        @update:model-value="(val) => project.pool_fees = val/100"
        :model-value="project.pool_fees*100"
      />
      <v-text-field
        v-bind="projectStructure.tax_rate"
        @update:model-value="(val) => project.tax_rate = val/100"
        :model-value="project.tax_rate*100"
      />
      </v-sheet>
    </v-sheet>
    <v-divider></v-divider>
    <v-expansion-panels
      v-model="tempPanel"
    >
      <v-expansion-panel
        elevation="0"
      >
        <v-expansion-panel-title>
          Air Temperature
          <template v-slot:actions="{ expanded }">
            <v-icon :icon="expanded ? 'mdi-check' : 'mdi-close'"></v-icon>
          </template>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-sheet
            class="d-flex justify-space-around mx-3"
          >
            <v-sheet
              min-width="200"
            >
              <v-combobox
                v-model="region"
                :items="stationStore.regions"
                label="Region"
                density="compact"
                class="mt-0"
                outlined
              />
            </v-sheet>
            <v-sheet
              min-width="200"
            >
              <v-combobox
                v-model="station"
                :items="stations"
                item-title="location"
                item-value="id"
                label="Weather Station"
                density="compact"
                class="mt-0"
                outlined
              />
            </v-sheet>
          </v-sheet>
          <v-container class="ma-0 pa-0 pl-3 pr-3 pb-6">
            <v-card
              v-if="!loadState || loadState.isLoading"
              elevation="0"
              class="d-flex justify-center align-center"
              min-height="510px"
            >
              <v-sheet>
                <v-progress-circular
                  color="secondary"
                  indeterminate
                ></v-progress-circular>
              </v-sheet>
            </v-card>
            <ChartScroll
              v-else
              :num-objects="stations?.length"
              v-model:objects-index="stationIndex"
            >
              <template #chart>
                <BaseChart
                  v-if="chartArgs"
                  v-bind="chartArgs"
                />
              </template>
            </ChartScroll>
          </v-container>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-divider></v-divider>
    <v-card-subtitle class="my-3">Rigs</v-card-subtitle>
    <v-btn variant="flat" icon="mdi-plus" @click="addRigs"/>
    <v-sheet class="mt-3 mx-3">
      <div v-for="(rig, i) in project.rigs" :key="'rig-'+ i">
        <ProjectFormRigSection
          :rig="rig"
          @update:rig="(id) => updateRigId(i, id)"
          @delete="(id) => deleteRig(i, id)"
          density="compact"
        />
      </div>
    </v-sheet>
    <v-divider></v-divider>
    <v-card-subtitle class="mt-3">Infrastructure</v-card-subtitle>
    <v-btn variant="flat" icon="mdi-plus" @click="addInfrastructure"/>
    <v-sheet class="mt-3 mx-3">
      <div v-for="(infra, i) in project.infrastructure" :key="'infra-'+ i">
        <ProjectFormInfraSection
          :type="project.infrastructure[i].infra_content_type"
          :infra="project.infrastructure[i]"
          @update:type="(type) => updateInfraType(i, type)"
          @update:infra="(id) => updateInfraObjectId(i, id)"
          @delete="(id) => deleteInfra(i, id)"
          density="compact"
        />
      </div>
    </v-sheet>
    <v-divider></v-divider>
    <v-row>
      <v-col>
          <v-card-subtitle class="mt-3">Building</v-card-subtitle>
          <v-sheet class="mt-3 mx-3">
          <v-text-field
            v-bind="projectStructure.buildingSize"
            v-model="project.buildingSize"
            class="mx-1"
          />
          <v-text-field
            v-bind="projectStructure.buildingCost"
            v-model="project.buildingCost"
            class="mx-1"
          />
        </v-sheet>          
      </v-col>
      <v-divider vertical/>
      <v-col>
        <v-card-subtitle class="mt-3">Operating</v-card-subtitle>
        <v-sheet
          class="mt-3 mx-3"
        >
          <v-text-field
            v-bind="projectStructure.opex"
            v-model="project.opex"
            class="mx-1"
          />
          <v-text-field
            v-bind="projectStructure.taxRate"
            v-model="project.taxRate"
            class="mx-1"
          />
        </v-sheet>
      </v-col>
    </v-row>
  </v-form>
</template>
  
  
<style scoped>
  :deep(.v-expansion-panel--active > .v-expansion-panel-title){
    min-height: 48px !important;
  }
  :deep(.v-expansion-panel-title--active > .v-expansion-panel-title__overlay) {
    opacity: 0;
  }
</style>