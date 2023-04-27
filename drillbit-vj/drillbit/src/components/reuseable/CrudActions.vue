<script setup>
import { ref, toRefs, computed, watch, watchEffect } from 'vue'
// import { promiseTimeout, useTimeout } from '@vueuse/core'

const props = defineProps({
  hasSelections: Boolean,
  disableCSV: {type: Boolean, default: false},
})
const { saveState } = toRefs(props)

const btnProps = {
  elevation: 0,
  size: 'x-small',
  class: 'mx-0',
}

// 'save', 'undo', 'redo'
const emit = defineEmits([
'add', 'delete', 'export:csv'
])
const emitAddNew = () => {
  emit('add')
}
const emitDelete = () => {
  emit('delete')
}
const emitCSV = () => {
  emit('export:csv')
}
// const emitSave = () => {
//   emit('save')
// }
// const emitUndo = () => {
//   emit('undo')
// }
// const emitRedo = () => {
//   emit('redo')
// }
// const saveSuccess = ref(false)
// const saveError = ref(false)

// watch(saveState, (saveState, oldState) => {
//   if (saveState.error?.value) {
//     saveError.value = true
//     promiseTimeout(1000).then(() => {
//       saveError.value = false
//       saveSuccess.value = false
//     })
//   } else if ( saveState.isReady.value ) {
//     saveSuccess.value = true
//     promiseTimeout(1000).then(() => {
//       saveSuccess.value = false
//     })
//   }
// }, {deep: true}
// )
</script>

<template>
  <v-toolbar color="surface" density="compact">
    <v-btn 
      icon="mdi-plus" 
      v-bind="btnProps" 
      @click="emitAddNew"
    />
    <v-btn 
      icon="mdi-delete" 
      v-bind="btnProps" 
      :disabled="!props.hasSelections" 
      @click="emitDelete"
    />
    <v-btn 
      icon="mdi-file-delimited"
      v-bind="btnProps"
      :disabled="disableCSV"
      @click="emitCSV"
    />
  </v-toolbar>
</template>
    
<style>
</style>