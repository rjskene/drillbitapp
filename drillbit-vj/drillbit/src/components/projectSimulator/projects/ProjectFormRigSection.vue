<script setup>
import { ref, computed, toRefs } from 'vue'
import { useVModel } from '@vueuse/core'
import { useGlobalStateStore } from '@/stores/globalState'
import { useRigStore } from '@/stores/modules'
import { useFormatHelpers, useFormHelpers } from '@/services/composables'

const globalState = useGlobalStateStore()
const store = useRigStore()
const format = useFormatHelpers()

const props = defineProps({
  objectId: {
    required: true,
  }
})

const items = computed(() => {
  return store.objects
})
const emit = defineEmits(['update:objectId', 'delete'])
const objectId = useVModel(props, 'objectId', emit)
const emitDelete = () => {
  emit('delete', objectId.value)
}

const findObjectById = (id) => {
  return store.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(objectId.value)
})
</script>
  
<template>
  <v-row>
    <v-col cols="4">
      <v-select
        v-model="objectId"
        v-bind="$attrs"
        :items="items"
        label="Rig name"
        item-title="name"
        item-value="id"
        class="mr-3"
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
    <v-col cols="2" class="d-flex align-center pl-12 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">Power:</span>
      {{format.power(object?.power)}}
    </v-col>
    <v-col cols="3" class="d-flex align-center pl-12 pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">Hash Rate:</span>
      {{format.hashRate(object?.hash_rate)}}
    </v-col>
    <v-col cols="2" class="d-flex align-center pt-0">
      <span class="text-body-2 text-medium-emphasis mr-3">Price:</span>
      {{format.currency(object?.price)}}
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>