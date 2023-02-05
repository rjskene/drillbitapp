<script setup>
import { ref, toRefs, computed, watch, watchEffect } from 'vue'
import { promiseTimeout, useTimeout } from '@vueuse/core'

const props = defineProps({
  hasSelections: Boolean,
  disableAdd: Boolean,
  saveState: {
    type: Object,
    default: () => {},
  },
  dtable: {type: Object, default: null},
})
const { saveState } = toRefs(props)

const btnProps = {
  elevation: 0,
  size: 'x-small',
  class: 'mx-0',
}

const emit = defineEmits(['save', 'delete:selections', 'add:new', 'undo', 'redo'])
const emitAddNew = () => {
  emit('add:new')
}
const emitDelete = () => {
  emit('delete:selections')
}
const emitSave = () => {
  emit('save')
}
const emitUndo = () => {
  emit('undo')
}
const emitRedo = () => {
  emit('redo')
}
const saveSuccess = ref(false)
const saveError = ref(false)
const isLoading = computed(() =>{
  return saveState.value.isLoading?.value
})

watch(saveState, (saveState, oldState) => {
  if (saveState.error?.value) {
    saveError.value = true
    promiseTimeout(1000).then(() => {
      saveError.value = false
      saveSuccess.value = false
    })
  } else if ( saveState.isReady.value ) {
    saveSuccess.value = true
    promiseTimeout(1000).then(() => {
      saveSuccess.value = false
    })
  }
}, {deep: true}
)
</script>

<template>
  <v-toolbar color="surface" density="compact">
    <v-btn 
      icon="mdi-plus" 
      v-bind="btnProps" 
      :disabled="props.disableAdd" 
      @click="emitAddNew"
    />
    <v-btn 
      icon="mdi-delete" 
      v-bind="btnProps" 
      :disabled="!props.hasSelections" 
      @click="emitDelete"
    />
    <v-btn 
      v-if="dtable !== null"
      icon="mdi-file-delimited"
      v-bind="btnProps" 
      @click="dtable.exportCSV()"
    />
    <v-btn 
      v-bind="btnProps"
      @click="emitSave"
    >
      <slot>
        <v-slide-x-transition :hide-on-leave="true">
          <v-icon v-if="saveError" :v-bind="btnProps" color="red">mdi-alert-circle-outline</v-icon>
          <v-icon v-else-if="saveSuccess" :v-bind="btnProps" color="green">mdi-check</v-icon>
          <v-icon v-else>mdi-content-save</v-icon>
        </v-slide-x-transition>
      </slot>
    </v-btn>
    <v-btn
      icon="mdi-undo"
      v-bind="btnProps"
      @click="emitUndo"
    />
    <v-btn
      icon="mdi-redo"
      v-bind="btnProps"
      @click="emitRedo"
    />
  </v-toolbar>
</template>
    
<style>
</style>