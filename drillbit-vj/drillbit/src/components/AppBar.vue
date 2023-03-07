<script setup>
import BTCSummaryBtn from '@/components/BTCSummaryBtn.vue'
import { useGlobalStateStore } from '../stores/globalState'

const globalState = useGlobalStateStore()

const toggleDrawer = () => {
  globalState.$patch({drawer: !globalState.drawer})
}
const clearStorage = () => {
  localStorage.clear()
  sessionStorage.clear()
  window.location.reload()
}
</script>
    
<template>
  <v-app-bar absolute clipped-right flat 
    height="48"
    color="primary"
  >
    <v-app-bar-nav-icon
      @click="toggleDrawer"
    />
    <v-toolbar-title class="font-weight-bold">DrillBit</v-toolbar-title>
    <BTCSummaryBtn/>
    <v-btn
      icon="mdi-trash-can-outline"
      @click="clearStorage"
    />
  </v-app-bar>
</template>
        
<style scoped>
</style>