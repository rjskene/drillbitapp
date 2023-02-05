import { createRouter, createWebHistory } from 'vue-router'
import { navRoutes } from '@/stores/globalState'

const staticRoutes = [
  // {
  //   path: '/',
  //   name: 'dashboard',
  //   component: DashboardView
  // }
]
const lazyRoutes = []

navRoutes.forEach(route => {
  lazyRoutes.push({
    path: route.link,
    name: route.name,
    component: () => import(`../views/${route.text.replace(' ', '')}View.vue`)  
  })
})
const routes = staticRoutes.concat(lazyRoutes)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
