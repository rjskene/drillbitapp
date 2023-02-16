<script setup>
import { ref, computed, toRefs } from 'vue'
import { useVModel } from '@vueuse/core'
import { useGlobalStateStore } from '../../stores/globalState'
import { 
  useCoolingStore,
  useRejectionStore,
  useElectricalStore,

} from '@/stores/modules'
import { useFormatHelpers, useFormHelpers } from '@/services/composables'

const globalState = useGlobalStateStore()
const coolingStore = useCoolingStore()
const rejectionStore = useRejectionStore()
const electricalStore = useElectricalStore()
const format = useFormatHelpers()

const props = defineProps({
  type: {
    required: true,
  },
  objectId: {
    required: true,
  }
})

const store = computed(() => {
  switch (props.type) {
    case 'cooling':
      return coolingStore
    case 'heatrejection':
      return rejectionStore
    case 'electrical':
      return electricalStore
    default:
      return null
  }
})

const items = computed(() => {
  return store.value.objects
})
const emit = defineEmits(['update:type', 'update:objectId', 'delete'])
const type = useVModel(props, 'type', emit)
const objectId = useVModel(props, 'objectId', emit)
const emitDelete = () => {
  emit('delete', objectId.value)
}

const findObjectById = (id) => {
  return store.value.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(objectId.value)
})
</script>
  
<template>
  <v-row>
    <v-col cols="3">
      <v-select
        v-model="type"
        v-bind="$attrs"
        :items="globalState.infraTypes"
        label="Type"
        item-title="title"
        item-value="value"
        required
      >
        <template #prepend>
          <v-btn
            @click="emitDelete"
            variant="flat"
            icon="mdi-delete"
            size="x-small"
          />
        </template>
      </v-select>
    </v-col>
    <v-col cols="3">
      <v-select
        v-model="objectId"
        v-bind="$attrs"
        :items="items"
        label="Name"
        item-title="name"
        item-value="id" 
        required
      />
    </v-col>
    <v-col cols="2" class="d-flex align-center pl-12 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">Power:</span>
      {{ format.power(object?.power) }}
    </v-col>
    <v-col cols="1" class="d-flex align-center pl-6 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">PUE:</span>
      {{object?.pue}}x
    </v-col>
    <v-col cols="3" class="d-flex align-center pl-12 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">Price:</span>
      {{format.currency(object?.price)}}
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>