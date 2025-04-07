import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import ChatView from '@/views/ChatView.vue'
import SyntheticDataView from '@/views/SyntheticDataView.vue'
import DashboardView from '@/views/DashboardView.vue'
import FileManagerView from '@/views/FileManagerView.vue'
import DetailReportView from '@/views/DetailReportView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
    },
    {
      path: '/synthetic-data',
      name: 'synthetic-data',
      component: SyntheticDataView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/file-manager',
      name: 'file-manager',
      component: FileManagerView,
    },
    {
      path: '/detail-report',
      name: 'detail-report',
      component: DetailReportView,
    },
  ],
})

export default router
