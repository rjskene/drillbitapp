<script setup>
import { computed, ref, watch } from 'vue'
import { useProjectStore, useProjectsStore } from '../stores/modules';

const projStore = useProjectStore()
const projsStore = useProjectsStore()
</script>
  
  
<template>
  {{ projsStore.objects }}
</template>
  
  
<style scoped>
  
</style>