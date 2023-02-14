<script setup>
import { ref, computed, toRefs } from 'vue'
import { useVModel } from '@vueuse/core'
import { useGlobalStateStore } from '../../stores/globalState'
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
const emit = defineEmits(['update:objectId'])
const objectId = useVModel(props, 'objectId', emit)

const findObjectById = (id) => {
  return store.findObjectById(id)
}
const object = computed(() => {
  return findObjectById(objectId.value)
})
</script>
  
<template>
  <v-row>
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
    <v-col class="ma-0 px-0">
      <v-card-subtitle class="inline">Power:</v-card-subtitle>
      {{format.power(object?.power)}}
    </v-col>
    <v-col cols="2" class="ma-0 px-0">
      <v-card-subtitle class="inline">Hash Rate:</v-card-subtitle>
      {{format.hashRate(object?.hash_rate)}}
    </v-col>
    <v-col>
      <v-card-subtitle class="inline">Price: </v-card-subtitle>
      {{format.currency(object?.price)}}
    </v-col>
  </v-row>
</template>
  
  
<style scoped>
  
</style>