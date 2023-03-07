<script setup>
import { toRefs, computed, defineProps } from 'vue'

import RejectionCurveChart from './RejectionCurveChart.vue'

import { useCurveStore } from '@/stores/modules'

const curveStore = useCurveStore()

const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
})
const {id, args} = toRefs(props)

const activatorId = computed(() => `rejection-curve-activator-${id.value}`)
const activator = computed(() => `#${activatorId.value}`)
</script>

<template>
  <v-btn
    :id="activatorId"
    @click="curveStore.getObject({pk: id})"
    icon="mdi-image-outline"
    variant="flat"
    v-bind="$attrs"
  />
  <v-menu 
    :activator="activator"
    :close-on-content-click="false"
  >
    <v-card 
      min-width="600" 
      min-height="400"
      class="rounded-xl card-border"
    >
      <v-card-title>Cooling Capacity</v-card-title>
      <v-sheet class="mx-3 px-6">
        <RejectionCurveChart
          v-if="curveStore.object"
          :object="curveStore.object"
        />
      </v-sheet>
    </v-card>
  </v-menu>
</template>

<style scoped>
:deep(.card-border) {
  border: 1px solid rgb(var(--v-theme-surface-12dp));
}
</style>