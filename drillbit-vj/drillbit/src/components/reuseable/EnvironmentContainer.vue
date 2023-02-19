<script setup>
import { ref, toRefs, watchEffect, computed } from 'vue'
import { storeToRefs } from 'pinia'

import CrudBar from './CrudBar.vue'

import { useEnvironmentStore} from '@/stores/modules'

const store = useEnvironmentStore()

const { lockable, locked } = storeToRefs(store)

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  onSave: {
    type: Function,
    default: () => {}
  },
})

const formValid = computed(() => {
  return form.value.errors.length === 0
})
const inputLocked = computed(() => {
  return locked.value[props.name]
})
const inputLockable = computed(() => {
  return lockable.value[props.name]
})

const form = ref(null)

const lock = async () => {
  if (inputLockable.value & formValid.value) {
    store.$patch(() => {
      store.locked[props.name] = true
    })
  }
}
const unlock = () => {
  store.$patch(() => {
    store.locked[props.name] = false
  })
}
</script>
  
<template>
  <v-container fluid class="full-height mt-3">
    <v-row class="">
      <v-col cols="12">
        <v-row>
          <v-col cols="1" class="pl-6 pr-0 mr-0">
          
          </v-col>
          <v-col cols="11" class="ml-0 pl-0">
            <v-form ref="form">
              <v-sheet
                class="d-flex justify-space-between align-center"
              >
                <CrudBar
                  @lock="lock"
                  @unlock="unlock"
                  :locked="inputLocked"
                  :lock-disabled="!inputLockable"
                  :save-disabled="inputLocked"
                  :on-save="onSave"
                />
                <slot name="fields"></slot>
              </v-sheet>
            </v-form>
          </v-col>
        </v-row>
        <v-row>
            <v-col class="mt-12 mx-6">
              <slot name="chart"></slot>
            </v-col>
        </v-row>
      </v-col>
    </v-row>      
  </v-container>
</template>
  
<style scoped>
:deep(.v-field__input) {
  min-height: 0px;
  max-height: 24px;
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