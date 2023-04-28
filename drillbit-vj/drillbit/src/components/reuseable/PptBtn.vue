<script setup>
import { ref, computed, toRefs } from 'vue'
import { createPPTX } from '../../services/ppt'

import {
  useEnvironmentStore,
} from '@/stores/modules'

const props = defineProps({
  environment: {
    type: Object,
    required: true,
  },
  group: {
    type: Object,
    required: true,
  },
  summary: {
    type: Object,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const store = useEnvironmentStore()
const { disabled } = toRefs(props)
const loading = ref(false)

const create = async () => {
  loading.value = true
  for (let element of store.elements) {
    let objId = props.environment[element.key]
    await element.store.getObject({pk: objId})
  }
  createPPTX(
    store.elements, 
    props.group, 
    props.summary,
  ).then(() => {
    loading.value = false
  })
}

</script>
  
  
<template>
  <v-btn
    @click="create"
    variant="outlined"
    size="x-large"
    icon="mdi-file-powerpoint-outline"
    :disabled="disabled"
    :loading="loading"
  ></v-btn>  
</template>
  
  
<style scoped>
  
</style>