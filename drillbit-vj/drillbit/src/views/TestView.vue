<script setup>
import { useAsyncState } from '@vueuse/core'

import { useRigStore } from '@/stores/modules'

const objects = [
  {a: 'test', b: 'object'},
  {a: 'different', b: 'values'}
]
const filter = () => {
  return objects.map((v, i, arr) => {
    return v.a
  })
}
const test = filter()
</script>
  {{test}}
  
<template>


</template>
  
  
<style scoped>
  
</style>