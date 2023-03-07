<script setup>
import { ref, toRefs, computed, defineProps, defineEmits, defineExpose } from 'vue'

import SimpleTable from '@/components/reuseable/SimpleTable.vue'
import { useFormatHelpers, TableMaker } from '@/services/composables'

const format = useFormatHelpers()

const props = defineProps(
  {
    costs: {
      type: Array,
      required: true
    },
  }
)

const columns = computed(() => {
  let cols = [
  {
    field: 'name',
    header: 'Name', 
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
  },
  {
    field: 'price',
    header: 'Price',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: format.currency,
  },
  {
    field: 'quantity',
    header: 'Quantity',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-7dot5',
    bodyFunc: format.number,
  },
  {
    field: 'total_cost',
    header: 'Cost',
    headerClass: 'table-header-center',
    bodyClass: 'table-body-center min-col-width-10',
    bodyFunc: format.currency,
  },
]
  let table = new TableMaker(cols)
  return table.columns
})
</script>
  
<template>
  <SimpleTable :data="costs" :columns="columns"/>
</template>
  
<style scoped>
  
</style>