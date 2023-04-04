<script setup>
  import { defineProps, onMounted, onBeforeUnmount, shallowRef } from 'vue'
  import { Line } from 'vue-chartjs'
  import sp500 from '../sp500.js'

  import vuetify from '@/services/vuetify'
  import { hexToRGB } from '@/services/composables'

  const props = defineProps({
    'min-width': {
      type: Number,
      default: 600
    },
    'min-height': {
      type: Number,
      default: 400
    },
  })
  const baseChartData = {
    'labels': [...Array(sp500.length).keys()],
    'datasets': [
      {
        'data': sp500.reverse(),
        borderColor: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .025, true),
      }
    ]
  } 

  function yValue(ctx, label) {
    const chart = ctx.chart;
    const dataset = chart.data.datasets[0];
    return dataset.data[chart.data.labels.indexOf(label)];
  }
  const text = {
    type: 'label',
    borderColor: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true),
    color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .7, true),
    backgroundColor: (ctx) => hexToRGB(vuetify.theme.current.value.colors['on-surface'], .01, true),
    borderRadius: 6,
    borderWidth: 1,
    font: {
      size: 36
    },
    content: ['Chart Will', 'Display Here'],
    position: {
      x: 'center',
      y: 'center'
    },
    xValue: 225,
    yValue: (ctx) => yValue(ctx, 200)
  }
  const box = {
    // Indicates the type of annotation
    type: 'box',
    xMin: 100,
    xMax: 325,
    yMin: 3200,
    yMax: 4200,
    backgroundColor: 'rgba(0,0,0,.1)'
  }
  const baseChartOptions = {
    maintainAspectRatio: false,
    plugins: {
      legend: {display: false},
      annotation: {
        annotations: {
          text,
          // box,
        }
      }
    },
    elements: {
      point: {
        radius: 0
      }
    },
    scales: {
      x: {
        border: {
          color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
        },
        grid: {
          display: false,
        },
        ticks: { 
          display: false,
        },
      },
      y: {
        beginAtZero: false,
        border: {
          color: hexToRGB(vuetify.theme.current.value.colors['on-surface'], .15, true)
        },
        grid: {
          display: false,
        },
        ticks: { 
          display: false,
        }
      }
    }
  }
</script>
  
<template>
  <Line :data="baseChartData" :options="baseChartOptions"/>
</template>

<style scoped>

</style>
