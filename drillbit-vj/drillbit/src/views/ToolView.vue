<script setup>
  import { ref } from 'vue'

  import ToolInputs from '../components/ToolInputs.vue'

  const tabs = [
    {text: 'Inputs', component: ToolInputs},
    {text: 'Results'}
  ]
  const currentTab = ref('Inputs')
</script>
  
  
<template>
  <v-card class="ma-10 pa-0 rounded-xl" min-height="1200px">
    <v-tabs
      v-model="currentTab"
      bg-color="background"
    >
        <v-tab
          v-for="tab in tabs"
          :key="tab + '-Tab'"
          :value="tab.text"
          class="tab-color-surface rounded-t-xl"
          slider-color="primary-variant-1"
        >{{ tab.text }}
        </v-tab>
      </v-tabs>
    <v-window
      v-model="currentTab"
      color="surface-lighten-1"
      class="ma-3"
      >
        <v-window-item
          v-for="tab in tabs"
          :key="tab + '-Window'"
          :value="tab.text"
        >
          <component :is="tab.component" />
        </v-window-item>
      </v-window>
  </v-card>
</template>
  
  
<style scoped>
:deep(.tab-color-surface) {
  background-color: rgb(var(--v-theme-surface));

}
</style>