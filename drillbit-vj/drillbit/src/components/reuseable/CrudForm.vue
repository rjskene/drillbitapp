<script setup>
import { ref, toRefs, watchEffect } from 'vue'
import CrudBar from './CrudBar.vue'

const props = defineProps({
  ready: {
    type: Boolean,
    required: true
  }
})
const { ready } = toRefs(props)
const form = ref(null)
const locked = ref(false)
const valid = ref(false)

const lock = async () => {
  let res = await form.value.validate()
  if (res.valid) {
    valid.value = true
  } else {
    valid.value = false
  }
}

defineExpose({ valid, locked })
watchEffect(() => {
  if (ready.value) {
    locked.value = true
  } else {
    locked.value = false
  }
})
</script>
  
<template>
  <v-sheet class="mt-3 pt-3 pr-3">
    <v-row>
      <v-col cols="1" class="mr-3 pr-1">
        <CrudBar 
          @lock="lock" 
          @unlock="locked = false"
          :locked="locked"
        />
      </v-col>
      <v-col cols="9" class="ml-0 mt-2 pl-0">
        <v-form ref="form">
          <slot name="fields"></slot>
        </v-form>
      </v-col>
    </v-row>
  </v-sheet>
</template>
  
<style scoped>
/* .v-sheet {
  border: 1px solid rgb(var(--v-theme-surface-lighten-24));
} */
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