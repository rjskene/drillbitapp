<script setup>
import { useGlobalStateStore } from '@/stores/globalState'
const globalState = useGlobalStateStore()
</script>
    
<template>
  <v-navigation-drawer
    color="surface-darken-1"
    absolute
    v-model="globalState.drawer"
    permanent
    class="grc-app-border"
  >
    <v-list
      nav
      height="250"
    >
      <v-list-item
        v-for="(item, i) in globalState.routes"
        link
        :to="item.link"
        :key="i"
        class="font-weight-medium"
      >
        {{item.text}}
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
    
    
<style scoped>
    
</style>