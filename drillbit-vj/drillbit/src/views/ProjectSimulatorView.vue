<script setup>
  import { ref } from 'vue'
  import { useAsyncState } from '@vueuse/core'

  import MainWindow from '@/components/projectSimulator/MainWindow.vue'
  import EnvironmentWindow from '../components/projectSimulator/environment/EnvironmentWindow.vue'
  import ProjectWindow from '../components/projectSimulator/projects/ProjectWindow.vue'
  import SimWindow from '../components/projectSimulator/sim/SimWindow.vue'
  import { useCurrentStateStore } from '@/stores/modules'
  import { useFormatHelpers } from '@/services/composables'


  const stateStore = useCurrentStateStore()
  const formatHelpers = useFormatHelpers()

  const tabs = [
    {text: 'Environment', component: EnvironmentWindow},
    {text: 'Projects', component: ProjectWindow},
    {text: 'Simulation', component: SimWindow}
  ]
  const currentTab = ref('Environment')

  const formatValue = (key, value) => {
    if (key === 'Price') return formatHelpers.currency(value)
    if (key === 'Reward') return formatHelpers.BTC(value)
    if (key === 'Difficulty') return formatHelpers.T(value)

    return value
  }
  
  const updateState = ref(null)
  const stateUpdate = () => {
    let state = useAsyncState(
      stateStore.getObjects({update: true}),
      {},
      {
        onError: (error) => {
          console.error(error.response)
        }
      }
    )
    updateState.value = state
  return state
}

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
      <v-btn
        id="btc-summary-activator"
        @click="stateStore.getObjects()"
        class="ml-auto"
        icon="mdi-currency-btc"
        variant="flat"
        color="background"
      />
      <v-menu 
        activator="#btc-summary-activator"
        :close-on-content-click="false"
      >
        <v-card min-width="400" class="rounded-xl">
          <v-card-title>Summary
            <v-btn 
              @click="stateUpdate"
              :loading="updateState?.isLoading"
              icon="mdi-reload"
              variant="flat"
              size="small"
            />
          </v-card-title>
          <v-card-text>
            <v-sheet
              v-for="(value, key) in stateStore.objects"
              class="d-flex justify-space-between"
            >
              <v-sheet>
                <v-card-subtitle>{{ key }}</v-card-subtitle>
              </v-sheet>
              <v-sheet>
                {{ formatValue(key, value) }}
              </v-sheet>
            </v-sheet>
          </v-card-text>
        </v-card>
      </v-menu>

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