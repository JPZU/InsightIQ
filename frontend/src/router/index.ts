import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ChatView from '@/views/ChatView.vue'
import DetailReportView from '@/views/DetailReportView.vue'

import AdminHomeView from '@/views/admin/AdminHomeView.vue'
import SyntheticDataView from '@/views/admin/SyntheticDataView.vue'
import FileManagerView from '@/views/admin/FileManagerView.vue'
// Si prefieres usar FileManagerView fuera del admin, cambia el import:
// import FileManagerView from '@/views/FileManagerView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Home',
      },
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
      meta: {
        title: 'Chat',
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        title: 'Dashboard',
      },
    },
    {
      path: '/admin',
      children: [
        {
          path: '',
          name: 'admin-home',
          component: AdminHomeView,
          meta: {
            title: 'Admin Home',
          },
        },
        {
          path: 'synthetic-data',
          name: 'synthetic-data',
          component: SyntheticDataView,
          meta: {
            title: 'Synthetic Data',
          },
        },
        {
          path: 'file-manager',
          name: 'file-manager',
          component: FileManagerView,
          meta: {
            title: 'File Manager',
          },
        },
      ],
    },
    {
      path: '/detail-report',
      name: 'detail-report',
      component: DetailReportView,
      meta: {
        title: 'Detailed Report',
      },
    },
  ],
})

router.beforeEach((to, from) => {
  document.title = to.meta?.title ?? 'InsightIQ'
})

export default router
