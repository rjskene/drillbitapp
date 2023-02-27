import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export var navRoutes = [
  // {text: 'Tool', name:'tool', link:'/'},
  {text: 'Project Simulator', name:'sim', link:'/'},
  {text: 'Environments', name:'enviro', link: '/environments'},
  {text: 'Rigs', name:'rigs', link: '/rigs'},
  {text: 'Infrastructure', name:'infra', link: '/infrastructure'},
  {text: 'Test', name:'test', link: '/test'}
]

export const useGlobalStateStore = defineStore('globalState', () => {
  const drawer = ref(false)
  const routes = ref(navRoutes)

  const allowedTimeSeriesModels = [
    {'title': 'Constant'},
    {'title': 'CGR'},
    {'title': 'GBM'},  
  ]

  const infraTypes = [
    {'title': 'Cooling', 'value': 'cooling'},
    {'title': 'Heat Rejection', 'value': 'heatrejection'},
    {'title': 'Electrical', 'value': 'electrical'},
  ]

  return { 
    drawer, routes, allowedTimeSeriesModels, infraTypes
  }
})
