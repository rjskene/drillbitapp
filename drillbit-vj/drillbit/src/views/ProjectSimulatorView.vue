<script setup>
  import { ref } from 'vue'
  import { useAsyncState } from '@vueuse/core'

  import EnvironmentWindow from '../components/projectSimulator/environment/EnvironmentWindow.vue'
  import ProjectWindow from '../components/projectSimulator/projects/ProjectWindow.vue'
  import SimWindow from '../components/projectSimulator/sim/SimWindow.vue'
  import BTCSummaryBtn from '@/components/BTCSummaryBtn.vue'

  const tabs = [
    {text: 'Environment', component: EnvironmentWindow},
    {text: 'Projects', component: ProjectWindow},
    {text: 'Simulation', component: SimWindow}
  ]
  const currentTab = ref('Environment')

</script>
  
<template>
  <v-card 
    class="ma-10 pa-0 rounded-xl" 
    min-height="1200px"
    color="background"
  >
    <v-tabs
      v-model="currentTab"
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
      class="mt-6"
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