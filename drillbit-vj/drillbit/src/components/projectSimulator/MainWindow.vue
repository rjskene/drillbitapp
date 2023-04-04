<script setup>
</script>

<template>
  <v-container 
    fluid
    class="d-flex ma-0 pa-0 mt-3"
  >
    <v-row class="ma-0 pa-0">
      <v-col cols="3" class="h-100 ma-0 pa-0">
        <v-sheet
          class="ma-0 pa-0 pt-3 pb-3 rounded-xl"
        >
          <slot name="nav-panel"></slot>
        </v-sheet>
      </v-col>
      <v-col cols="8" class="ma-0 pa-0 ml-12">
        <v-card 
          class="ma-0 pa-0 pt-3 h-100 rounded-xl"
          min-height="680px"
          color="surface"
        >
          <slot name="main-panel"></slot>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
<style scoped>
:deep(.border-right) {
  border: 1px solid rgb(var(--v-theme-background));
}
</style>