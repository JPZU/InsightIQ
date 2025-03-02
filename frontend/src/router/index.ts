import { createRouter, createWebHistory } from 'vue-router'

import ChatView from '@/views/ChatView.vue'
import SyntheticDataView from '@/views/SyntheticDataView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'chat',
      component: ChatView,
    },
    {
      path: '/synthetic-data',
      name: 'synthetic-data',
      component: SyntheticDataView,
    },
  ],
})

export default router
