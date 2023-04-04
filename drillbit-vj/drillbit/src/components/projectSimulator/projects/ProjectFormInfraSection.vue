<script setup>
import { ref, computed, toRefs, watch } from 'vue'
import { useVModel } from '@vueuse/core'
import { useGlobalStateStore } from '@/stores/globalState'
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
  infra: {
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
  console.log('items', store.value.objects)
  return store.value.objects
})

const emit = defineEmits(['update:type', 'update:infra', 'delete'])
const type = useVModel(props, 'type', emit)
const infra = useVModel(props, 'infra', emit)
const emitDelete = () => {
  emit('delete', infra.value.infra_object_id)
}

const findObjectById = (id) => {
  return store.value.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(infra.value.infra_object_id)
})
watch(() => infra.value.infra_object_id, (infra_object_id) => {
  if (!infra.value.price)
    infra.value.price = object.value.price
})
</script>
  
<template>
  <v-row class="d-flex justify-space-between">
    <v-col cols="2" class="pl-2">
      <v-select
        v-model="type"
        v-bind="$attrs"
        :items="globalState.infraTypes"
        label="Type"
        item-title="title"
        item-value="value"
        required
        single-line
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
    <v-col cols="2" class="pl-0 ml-0">
      <v-select
        v-model="infra.infra_object_id"
        v-bind="$attrs"
        :items="items"
        label="Name"
        item-title="name"
        item-value="id" 
        required
        single-line
      />
    </v-col>
    <v-col class="d-flex align-center pl-1 pr-0 pt-0 ml-0 mr-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Power:</span>
      {{ format.power(object?.capacity) }}
    </v-col>
    <v-col class="d-flex align-center pl-1 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">PUE:</span>
      {{object?.pue}}x
    </v-col>
    <v-col class="d-flex align-center pl-0 pr-0 pt-0 ml-0 mr-0">
      <span class="text-body-2 text-medium-emphasis pl-0 ml-0">Price:</span>
      <v-text-field
        v-model="infra.price"
        type="number"
        prefix="$"
        density="compact"
        variant="plain"
        class="pl-1 pt-2"
        single-line
      />
    </v-col>
    <v-col class="d-flex align-center pl-1 pr-0 pt-0 ml-0 mr-0">
      <span class="text-body-2 text-medium-emphasis">Quantity:</span>
      <v-text-field
        v-model="infra.quantity"
        type="number"
        density="compact"
        variant="plain"
        class="pl-1 pt-2"
        single-line
      />
    </v-col>
    <v-col class="d-flex align-center pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Total Cost:</span>
      {{format.currency(infra.quantity * infra.price)}}
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>