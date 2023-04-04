<script setup>
  import { ref } from 'vue'
  import { useAsyncState } from '@vueuse/core'

  import { useCurrentStateStore } from '@/stores/modules'
  import { useFormatHelpers } from '@/services/composables'


  const stateStore = useCurrentStateStore()
  const formatHelpers = useFormatHelpers()

  const formatValue = (key, value) => {
    if (key === 'Price') return formatHelpers.currency(value)
    if (key === 'Reward') return formatHelpers.BTC(value)
    if (key === 'Difficulty') return formatHelpers.T(value)
    if (key === 'Network Hash Rate') return formatHelpers.hashRate(value, {toFixed: 2})

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
  <v-btn
    id="btc-summary-activator"
    @click="stateStore.getObjects()"
    class="ml-auto"
    icon="mdi-currency-btc"
    variant="flat"
    color="primary"
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
</template>
  
  
<style scoped>
</style>