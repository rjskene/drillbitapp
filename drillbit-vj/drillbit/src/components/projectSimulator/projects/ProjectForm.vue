<script setup>
import { ref, computed, toRefs, watch } from 'vue'
import { useRefHistory, useAsyncState } from '@vueuse/core'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
import ProjectFormInfraSection from './ProjectFormInfraSection.vue'
import ProjectFormRigSection from './ProjectFormRigSection.vue'
import ProjectCostsTable from './ProjectCostsTable.vue'

import { 
  useProjectStore,
  useRigStore, 
  useCoolingStore,
  useRejectionStore,
  useElectricalStore,
} from '@/stores/modules'

import { useFormatHelpers, useFormHelpers } from '@/services/composables'

const store = useProjectStore()
const rigStore = useRigStore()
const coolingStore = useCoolingStore()
const rejectionStore = useRejectionStore()
const electricalStore = useElectricalStore()

const { nameRules, numberRules, percentageRules } = useFormHelpers()
const format = useFormatHelpers()

const props = defineProps({
  project: {
    type: Object,
    default: null
  }
})

const projectStructure = computed(() => {
  return {
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
    'target_ambient_temp': {
      label: 'Temperature',
      suffix: '°F',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 96,
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
      default: [{'rig_id': null}],
      required: true,
    },
    infrastructure: {
      label: 'Infrastructure',
      required: true,
      default: [{infra_content_type: 'cooling', infra_object_id: null}]
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
const createNewProject = () => {
  /* 
  creates a new object with keys same as projectStructure
  and values set to null, except where there is a default
  value in projectStructure
  */
  return Object.fromEntries(
    Object.entries(projectStructure.value).map(([key, value]) => {
      return [key, value.default ?? null]
    })
  )
}
const project = ref(
  props.project || createNewProject()
)
const saveState = ref(null)

const saveProject = () => {
  if (project.value && Object.keys(project.value).includes('id') && project.value.id)
    return  store.update(project.value)
  else {
    return store.create(project.value)
  }
}
const { history, undo, redo } = useRefHistory(project, {deep: true})
const rig = computed(() => {
  return rigStore.findObjectById(project.value.rig)
})

const addRigs = () => {
  project.value.rigs.push({rig_id: null})
}
const updateRigId = (index, id) => {
  project.value.rigs[index].rig_id = id
}
const deleteItemFromArrayBasedOnIndex = (array, index) => {
  array.splice(index, 1)
}
const deleteRig = (index, pk) => {
  project.value.rigs.splice(index, 1)
}
const addInfrastructure = () => {
  project.value.infrastructure.push({infra_content_type: 'cooling', infra_object_id: null})
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

watch(() => props.project, (newVal) => {
  project.value = newVal || createNewProject()
})

const costs = ref(null)
const updateCosts = (pk) => {
  store.scale(pk).then(async () => {
    costs.value = await store.costs(pk)
    console.log(costs.value)
  })
}
</script>
  
<template>
  <v-form>
    <v-card-title>{{ project?.name }}</v-card-title>
    <StatefulBtn
      @click="saveProject"
      variant="flat"
      icon="mdi-content-save"
    />
    <v-btn
      @click="undo"
      color="on-surface"
      variant="flat"
      icon="mdi-undo"
    />
    <v-btn
      @click="redo"
      color="on-surface"
      variant="flat"
      icon="mdi-redo"      
    />
      <v-sheet
        class="d-flex justify-left ml-3"
      >
          <v-text-field
            v-bind="projectStructure.name"
            v-model="project.name"
            class="pr-12"
          />
          <v-text-field
            v-bind="projectStructure.description"
            v-model="project.description"
            class="mx-3"
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
        />
      </v-sheet>
      <v-sheet
        class="d-flex flex-column justify-space-between"
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
    <v-card-subtitle class="my-3">Rigs</v-card-subtitle>
    <v-btn variant="flat" icon="mdi-plus" @click="addRigs"/>
    <v-sheet class="mt-3 mx-3">
      <div v-for="(rig, i) in project.rigs" :key="'rig-'+ i">
        <ProjectFormRigSection
          :object-id="project.rigs[i]['rig_id']"
          @update:object-id="(id) => updateRigId(i, id)"
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
          :object-id="project.infrastructure[i].infra_object_id"
          @update:type="(type) => updateInfraType(i, type)"
          @update:object-id="(id) => updateInfraObjectId(i, id)"
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
  <v-divider v-if="project.hasOwnProperty('id')"></v-divider>
  <v-row class="my-6" v-if="project.hasOwnProperty('id')">
    <v-col>
      <v-card-subtitle class="mt-3">Costs</v-card-subtitle>
      <v-btn
        @click="updateCosts(project.id)"
        variant="outlined"
        class="ml-3 my-3"
      >
        Scale
      </v-btn>
      <v-sheet class="mx-6">
        <ProjectCostsTable v-if="costs" :costs="costs" />
      </v-sheet>
    </v-col>
  </v-row>
</template>
  
  
<style scoped>

</style>