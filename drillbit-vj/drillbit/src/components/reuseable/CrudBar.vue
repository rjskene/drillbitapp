<script setup>
import { ref, toRefs, computed, watch } from 'vue'
import { useAsyncState, promiseTimeout } from '@vueuse/core'

import StatefulBtn from './StatefulBtn.vue'

const props = defineProps({
  locked: {
    type: Boolean,
    required: true
  },
  lockDisabled: {
    type: Boolean,
    default: false
  },
  saveDisabled: {
    type: Boolean,
    default: false
  },
  onSave: {
    type: Function,
    default: () => {}
  },
  actions: {
    type: Object,
    default: () => {return {add: false, open: false}}
  }
})
const { locked } = toRefs(props)

const btnProps = {
  elevation: "0",
  size: "large",
  variant: "flat",
  density: "compact",
}
const emit = defineEmits(['save', 'open', 'new', 'lock', 'unlock'])

const lock = () => {
  emit('lock')
}
const unlock = () => {
  emit('unlock')
}
</script>
  
<template>
  <v-sheet>
    <v-sheet>
      <v-btn
        v-if="props.actions.add"
        icon="mdi-plus"
        v-bind="btnProps"
        />
    </v-sheet>
    <v-sheet>
      <v-btn
        v-if="props.actions.open"
        icon="mdi-folder-open"
        v-bind="btnProps"
        />
    </v-sheet>
    <v-sheet>
      <StatefulBtn
        @click="onSave"
        v-bind="btnProps"
        :disabled="saveDisabled"
        icon="mdi-content-save"
      />
    </v-sheet>
    <v-sheet>
      <v-btn
        v-if="locked"
        @click="unlock"
        icon="mdi-lock"
        v-bind="btnProps"
      ></v-btn>
      <v-btn
        v-else
        @click="lock"
        :disabled="lockDisabled"
        icon="mdi-lock-open-variant"
        v-bind="btnProps"
      ></v-btn>
    </v-sheet>
</v-sheet>
</template>
  
  
<style scoped>

</style>