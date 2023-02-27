<!-- 
Custom Component for a button that can be used with useAsyncState

This button receives a method for the onClick event. The method will be wrapped in a useAsyncState instance,
if it is not already an instance of useAsyncState.
-->

<script setup>
import { computed, ref, watch } from 'vue'
import { useAsyncState, promiseTimeout } from '@vueuse/core'

const props = defineProps({
  onClick: {
    type: Function,
    required: true,
  },
  icon: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    required: false,
  },
  successIcon: {
    type: String,
    default: 'mdi-check',
  },
  errorIcon: {
    type: String,
    default: 'mdi-alert-circle-outline',
  },
})

const state = ref(null)
const success = ref(false)
const error = ref(false)

const btnClass = computed(() => {
  return {
    'v-btn--icon': props.label ? false : true,
  }
})

const objectIsAsyncState = (obj) => {
  console.log('obj', obj)
  return obj.hasOwnProperty('state') 
    && obj.hasOwnProperty('isLoading') 
    && obj.hasOwnProperty('isReady')
    && obj.hasOwnProperty('error')
}
const objectIsAsyncQueue = (obj) => {
  return obj.hasOwnProperty('activeIndex') 
    && obj.hasOwnProperty('result')
    && Object.keys(obj).length() === 2
    && obj.result instanceof Array
}

const onClick = () => {
  state.value = props.onClick()
  if (!objectIsAsyncState(state.value)) {
    state.value = useAsyncState(
      state.value,
      {},
      {
        onError: (error) => {
          console.error(error.response ?? error)
        }
      }
    )
  }
}
const isLoading = computed(() =>{
  return state.value.isLoading?.value
})
watch(state, (state, oldState) => {
  if (state.error) {
    error.value = true
    promiseTimeout(2000).then(() => {
      error.value = false
      success.value = false
    })
  } else if ( state.isReady ) {
    success.value = true
    promiseTimeout(2000).then(() => {
      success.value = false
    })
  }
}, {deep: true}
)
</script>
  
  
<template>
  <!-- v-btn--icon class is added b/c, when icons are added via default slot they lose the `v-btn--icon` class -->
  <v-btn
    @click="onClick"
    v-bind="$attrs"
    :loading="state?.isLoading"
    :class="btnClass"
  >
    <slot>
      <span v-if="props.label" class="mr-3">{{ props.label }}</span>
      <v-slide-x-transition :hide-on-leave="true">
        <v-icon v-if="error" color="red">{{props.errorIcon}}</v-icon>
        <v-icon v-else-if="success" color="green">{{ props.successIcon }}</v-icon>
        <v-icon v-else>{{props.icon}}</v-icon>
      </v-slide-x-transition>
    </slot>
  </v-btn>  
</template>

<style scoped>
  
</style>