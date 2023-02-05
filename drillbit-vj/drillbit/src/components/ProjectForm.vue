<script setup>
import { ref, computed, toRefs } from 'vue'

import { useProjectStore} from '../stores/modules'
import { useFormHelpers } from '../services/composables'

const store = useProjectStore()
const { nameRules, numberRules } = useFormHelpers()
const form = ref(null)

const props = defineProps({
  project: {
    type: Object,
    default: null
  }
})
// const { project } = toRefs(props)
const projectName = computed(() => {
  return props.project?.name || 'New Project'
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
    powerCapacity: {
      label: 'Power Capacity',
      suffix: 'MW',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 40,
    }, 
    powerCost: {
      label: 'Power Cost',
      suffix: '$/kWh',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 0.05,
    }, 
    overclocking:{
      label: 'Overclocking',
      suffix: 'x',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 1,
    }, 
    temperature: {
      label: 'Temperature',
      suffix: '°F',
      density: 'compact',
      required: true,
      rules: numberRules.value,
      default: 96,
    }, 
    rig: {
      label: 'Rig',
      density: 'compact',
      required: true,
    }, 
    cooling: {
      label: 'Cooling',
      density: 'compact',
      required: true,
    }, 
    rejection: {
      label: 'Heat Rejection',
      density: 'compact',
      required: true,
    }, 
    electrical: {
      label: 'Electrical',
      density: 'compact',
      required: true,
    },
    buildingSize: {
      label: 'Size in Square Feet',
      density: 'compact',
      suffix: 'ft²',
      rules: numberRules.value,
      default: 0,
    },
    buildingCost: {
      label: 'Cost per Square Foot',
      suffix: '$/ft²',
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
const newProject = ref(createNewProject())
const saveProject = async () => {
  let res = await form.value.validate()
  if (res.valid)
    if (props.project)
      store.$patch((state) => {
        state.projects[props.project.id] = newProject.value
      })
    else
      store.$patch((state) => {
        state.projects.push(newProject.value)
      })
}
store.$subscribe(() => {
  newProject.value = createNewProject()
})
const project = computed(() => {
  if (props.project) {
    return props.project
  } else {
    return newProject.value
  }
})
</script>
  
<template>
  <v-card 
    elevation=0
    class="border "
  >
    <v-card-title>{{ projectName }}</v-card-title>
    <v-btn 
      color="on-surface"
      @click="saveProject"
      variant="flat"
      icon="mdi-content-save"
      ></v-btn>
    <v-form ref="form">
      <v-sheet 
        class="d-flex justify-space-between"
      >
        <v-sheet
          class="d-flex flex-column justify-space-between"
          min-width="400"
        >
            <v-text-field
              v-bind="projectStructure.name"
              v-model="project.name"
            />
            <v-text-field
              v-bind="projectStructure.description"
              v-model="project.description"
            />
          </v-sheet>
        <v-sheet
          class="d-flex flex-column justify-space-between ml-12"
          min-width="200"
        >
          <v-text-field 
            v-bind="projectStructure.powerCapacity" 
            v-model="project.powerCapacity"
          />
          <v-text-field 
            v-bind="projectStructure.powerCost" 
            v-model="project.powerCost"
          />
        </v-sheet>
        <v-sheet
          class="d-flex flex-column justify-space-between"
          min-width="200"
        >
          <v-text-field 
            v-bind="projectStructure.overclocking" 
            v-model="project.overclocking"
          />
          <v-text-field 
            v-bind="projectStructure.temperature"
            v-model="project.temperature"
          />
        </v-sheet>
      </v-sheet>
      <v-divider></v-divider>
      <v-sheet class="mt-3">
        <v-select 
          v-bind="projectStructure.rig"
          v-model="project.rig"
        />
      </v-sheet>
      <v-divider></v-divider>
      <v-card-subtitle class="mt-3">Infrastructure</v-card-subtitle>
      <v-sheet 
        class="d-flex align-space-between mt-3"
      >
        <v-select 
          v-bind="projectStructure.cooling" 
          v-model="project.cooling"
          class="mx-1"
        />
        <v-select 
          v-bind="projectStructure.rejection" 
          v-model="project.rejection"
          class="mx-1"
        />
        <v-select 
          v-bind="projectStructure.electrical"
          v-model="project.electrical"
          class="mx-1"
        />
      </v-sheet>
      <v-divider></v-divider>
      <v-card-subtitle class="mt-3">Building</v-card-subtitle>
      <v-sheet 
      class="d-flex align-space-between mt-3"
      >
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
    <v-divider></v-divider>
      <v-card-subtitle class="mt-3">Operating</v-card-subtitle>
      <v-sheet 
        class="d-flex align-space-between mt-3"
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
      
    </v-form>
  </v-card>  
</template>
  
  
<style scoped>
.standard-border {
  border: 1px solid rgb(var(--v-theme-surface-lighten-24));
}
.textbox {
  max-height: 24px;
}
:deep(.v-field__input) {
  min-height: 0px;
  max-height: 12px;
}
:deep(.v-field-label) {
  top: 0px;
}
:deep(.v-field-label--floating) {
  visibility: hidden !important;
}
:deep(.v-field__field .v-field__input) {
  padding-bottom: 15px;
  padding-top: 15px;
}
:deep(.v-field__clearable) {
  padding-top: 2px;
}
:deep(.v-input__details) {
  padding-inline-start: 0px;
}
:deep(.v-text-field__prefix){
  padding-top: 3px !important;
  padding-bottom: 0px !important;
  padding-left: 3px !important;
}
:deep(.v-text-field__suffix){
  padding-top: 3px !important;
  padding-bottom: 0px !important;
  padding-left: 3px !important;
}
:deep(.v-select .v-field .v-field__field .v-field__input) {
  padding-top: 0px;
}
:deep(.v-field__append-inner) {
  padding-top: 3px;
  padding-bottom: 0px;
  padding-right: 0px;
}
</style>