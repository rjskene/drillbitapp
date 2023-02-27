import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import { Chart as ChartJS, registerables } from 'chart.js'

// ALL THIS PRIMEVUE STUFF FOR FREAKIN DATATABLE!!!!!
import "primevue/resources/themes/lara-light-blue/theme.css"
import "primevue/resources/primevue.min.css"
import "primeicons/primeicons.css"
import PrimeVue from 'primevue/config'


// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import vuetify from '@/services/vuetify'

// Pinia
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { productPlugin } from "@/stores/modules"



const pinia = createPinia()
pinia.use(productPlugin)
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(vuetify)
app.use(PrimeVue)

app.mount('#app')

import annotationPlugin from 'chartjs-plugin-annotation'

import { Colors } from 'chart.js';
console.log(Colors)
// Chart.register(Colors);

ChartJS.register(...registerables)
ChartJS.register(annotationPlugin)
// ChartJS.defaults.backgroundColor = vuetify.theme.themes.value.light.colors.blue
// ChartJS.defaults.borderColor = vuetify.theme.themes.value.dark.colors['on-surface']
ChartJS.defaults.color = vuetify.theme.themes.value.dark.colors['on-surface']
// ChartJS.defaults.color = vuetify.theme.themes.value.light.colors.blue