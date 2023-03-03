<script setup>
  import { useGlobalStateStore } from '../stores/globalState'
  const globalState = useGlobalStateStore()

  const toggleDrawer = () => {
    globalState.$patch({drawer: !globalState.drawer})
  }
  const clearStorage = () => {
    localStorage.clear()
    sessionStorage.clear()
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
    <v-btn
      icon="mdi-trash-can-outline"
      @click="clearStorage"
    />
  </v-app-bar>
</template>
        
<style scoped>
</style>