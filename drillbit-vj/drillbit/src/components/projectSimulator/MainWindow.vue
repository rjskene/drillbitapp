<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'

import StatefulBtn from '@/components/reuseable/StatefulBtn.vue'
// import BlockScheduleForm from './environment/BlockScheduleForm.vue'
// import BTCPriceForm from './environment/BTCPriceForm.vue'
// import TransactionFeesForm from './environment/TransactionFeesForm.vue'
// import NetworkHashRateForm from './environment/NetworkHashRateForm.vue'


</script>

<template>
  <v-container fluid class="ma-0 px-0">
    <v-row>
      <v-col cols="3">
        <v-list
          nav
          density="compact"
        >
          <slot name="nav-panel"></slot>
        </v-list>
      </v-col>
      <v-col cols="9" class="h-100">
        <v-card elevation="0" class="border rounded-xl ma-0 pa-5 h-100">
          <slot name="main-panel"></slot>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
<style scoped>
</style>