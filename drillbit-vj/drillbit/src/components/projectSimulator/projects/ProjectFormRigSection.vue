<script setup>
import { ref, computed, watch } from 'vue'
import { useVModel } from '@vueuse/core'
import { useRigStore } from '@/stores/modules'
import { useFormatHelpers } from '@/services/composables'

const store = useRigStore()
const format = useFormatHelpers()

const props = defineProps({
  rig: {
    required: true,
  }
})

const items = computed(() => {
  return store.objects
})
const emit = defineEmits(['update:rig', 'delete'])
const rig = useVModel(props, 'rig', emit)
const emitDelete = () => {
  emit('delete', rig.value.id)
}

const findObjectById = (id) => {
  return store.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(rig.value.rig_id)
})

watch(() => rig.value.rig_id, (rig_id) => {
  if (!rig.value.price)
    rig.value.price = object.value.price
})
</script>
  
<template>
  <v-row class="d-flex justify-space-between">
    <v-col cols="3" class="pl-2">
      <v-select
        v-model="rig.rig_id"
        v-bind="$attrs"
        :items="items"
        label="Rig name"
        item-title="name"
        item-value="id"
        class="mr-0"
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
    <v-col class="d-flex align-center pl-3 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Power:</span>
      {{format.power(object?.power, { toFixed: 2 })}}
    </v-col>
    <v-col class="d-flex align-center pl-3 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">HR:</span>
      {{format.hashRate(object?.hash_rate)}}
    </v-col>
    <v-col class="d-flex align-center pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Price:</span>
      <v-text-field
        v-model="rig.price"
        type="number"
        prefix="$"
        density="compact"
        variant="plain"
        class="pl-2 pt-2"
        single-line
      />
    </v-col>
    <v-col class="d-flex align-center pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Quantity:</span>
      <v-text-field
        v-model="rig.quantity"
        type="number"
        density="compact"
        variant="plain"
        class="pl-2 pt-2"
        single-line
      />
    </v-col>
    <v-col class="d-flex align-center pt-0">
      <span class="text-body-2 text-medium-emphasis mr-1">Total Cost:</span>
      {{format.currency(rig.quantity * rig.price)}}
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>