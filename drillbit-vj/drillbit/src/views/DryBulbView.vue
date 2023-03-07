<script setup>
import DryBulbScaler from '../components/DryBulbScaler.vue'
</script>
  
  
<template>
  <v-card 
    class="ma-10 pa-0 rounded-xl" 
    min-height="1200px"
    color="background"
  >
    <v-card-title>Design Dry Bulb Analysis</v-card-title>
    <DryBulbScaler/>
  </v-card>
</template>
  
  
<style scoped>
:deep(.tab-color-surface) {
  background-color: rgb(var(--v-theme-surface));

}
</style>