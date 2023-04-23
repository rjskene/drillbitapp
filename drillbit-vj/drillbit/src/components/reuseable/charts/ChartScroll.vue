<script setup>
import { computed, ref, toRefs } from 'vue'
import { useVModel } from '@vueuse/core'

const props = defineProps({
  numObjects: {
    type: Number,
    required: true,
  },
  objectsIndex: {
    type: Number,
    required: true,
  },
  scrollPosition: {
    type: String,
    default: 'bottom',
  },
})
const { numObjects } = toRefs(props)
const emit = defineEmits(['update:objectsIndex'])
const objectsIndex = useVModel(props, 'objectsIndex', emit)

const next = () => {
  objectsIndex.value = objectsIndex.value >= numObjects.value - 1 ? 0 : objectsIndex.value + 1
}
const prev = () => {
  objectsIndex.value = objectsIndex.value <= 0 ? numObjects.value - 1 : objectsIndex.value - 1
}

</script>

<template>
    <v-card
      elevation="0"
    >
    <v-card-actions v-if="props.scrollPosition === 'top'" class="justify-space-between">
        <v-btn
          variant="plain"
          icon="mdi-chevron-left"
          @click="prev"
        ></v-btn>
        <v-item-group
          v-if="numObjects < 10"
          v-model="objectsIndex"
          class="text-center"
          mandatory
        >
          <v-item
            v-for="n in numObjects"
            :key="`btn-${n - 1}`"
            v-slot="{ isSelected, toggle }"
            :value="n - 1"
          >
            <v-btn
              :variant="isSelected ? 'outlined' : 'text'"
              icon="mdi-record"
              @click="toggle"
            ></v-btn>
          </v-item>
        </v-item-group>
        <v-btn
          variant="plain"
          icon="mdi-chevron-right"
          @click="next"
        ></v-btn>
      </v-card-actions>
      <slot name="chart">
      </slot>
      <v-card-actions v-if="props.scrollPosition === 'bottom'" class="justify-space-between">
        <v-btn
          variant="plain"
          icon="mdi-chevron-left"
          @click="prev"
        ></v-btn>
        <v-item-group
          v-if="numObjects < 10"
          v-model="objectsIndex"
          class="text-center"
          mandatory
        >
          <v-item
            v-for="n in numObjects"
            :key="`btn-${n - 1}`"
            v-slot="{ isSelected, toggle }"
            :value="n - 1"
          >
            <v-btn
              :variant="isSelected ? 'outlined' : 'text'"
              icon="mdi-record"
              @click="toggle"
            ></v-btn>
          </v-item>
        </v-item-group>
        <v-btn
          variant="plain"
          icon="mdi-chevron-right"
          @click="next"
        ></v-btn>
      </v-card-actions>
    </v-card>
</template>
  
<style scoped>
</style>

