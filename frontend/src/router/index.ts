import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/LoginView.vue'

import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ChatView from '@/views/ChatView.vue'
import ReportView from '@/views/ReportView.vue'

import AdminHomeView from '@/views/admin/AdminHomeView.vue'
import SyntheticDataView from '@/views/admin/SyntheticDataView.vue'
import FileManagerView from '@/views/admin/FileManagerView.vue'
import AlarmCreateView from '@/views/admin/AlarmCreateView.vue'
import AlarmListView from '@/views/admin/AlarmListView.vue'
import AlarmEditView from '@/views/admin/AlarmEditView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        title: 'Login',
      },
    },
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
      path: '/report',
      name: 'report',
      component: ReportView,
      meta: {
        title: ' Report',
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
        {
          path: 'alarm-create',
          name: 'alarm-create',
          component: AlarmCreateView,
          meta: {
            title: 'Create Alarm',
          },
        },
        {
          path: 'alarm-list',
          name: 'alarm-list',
          component: AlarmListView,
          meta: {
            title: 'List Alarms',
          },
        },
        {
          path: 'alarm-edit/:id',
          name: 'alarm-edit',
          component: AlarmEditView,
          meta: {
            title: 'Edit Alarm',
          },
          props: true,
        },
      ],
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView,
      meta: {
        title: 'Report',
      },
    },
  ],
})

router.beforeEach((to, from) => {
  document.title = to.meta?.title ?? 'InsightIQ'
})

export default router
