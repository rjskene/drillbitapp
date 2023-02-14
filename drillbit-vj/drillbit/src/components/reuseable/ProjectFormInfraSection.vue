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
const emit = defineEmits(['update:type', 'update:objectId'])
const type = useVModel(props, 'type', emit)
const objectId = useVModel(props, 'objectId', emit)

const findObjectById = (id) => {
  return store.value.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(objectId.value)
})
</script>
  
<template>
  <v-row>
    <v-col cols="2">
      <v-select
        v-model="type"
        v-bind="$attrs"
        :items="globalState.infraTypes"
        item-title="title"
        item-value="value"
        class="mr-3"
        required
      />
    </v-col>
    <v-col cols="3">
      <v-select
        v-model="objectId"
        v-bind="$attrs"
        :items="items"
        item-title="name"
        item-value="id"
        class="mr-3"
        required
      />
    </v-col>
    <v-col class="ma-0">
      <v-card-subtitle class="inline ma-0">Power:</v-card-subtitle>
      {{ format.power(object?.power) }}
    </v-col>
    <v-col class="ma-0">
      <v-card-subtitle class="inline">PUE:</v-card-subtitle>
      {{object?.pue}}x
    </v-col>
    <v-col>
      <v-card-subtitle class="inline">Price: </v-card-subtitle>
      {{format.currency(object?.price)}}
    </v-col>
    <!-- <v-col>
      <v-card-subtitle class="inline">Quantity: </v-card-subtitle>
    </v-col>
    <v-col>
      <v-card-subtitle class="inline">Total Cost: </v-card-subtitle>
    </v-col> -->
  </v-row>
</template>
  
  
<style scoped>
  
</style>