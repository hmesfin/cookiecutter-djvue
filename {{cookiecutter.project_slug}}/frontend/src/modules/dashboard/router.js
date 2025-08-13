import DashboardLayout from '@/layouts/DashboardLayout.vue'
import DashboardView from './views/DashboardView.vue'

export default [
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardView,
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('./views/ProfileView.vue'),
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('./views/SettingsView.vue'),
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('./views/AnalyticsView.vue'),
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('./views/UsersView.vue'),
      },
      {
        path: 'orders',
        children: [
          {
            path: '',
            name: 'Orders',
            component: () => import('./views/OrdersView.vue'),
          },
          {
            path: 'new',
            name: 'NewOrder',
            component: () => import('./views/NewOrderView.vue'),
          },
        ],
      },
    ],
  },
]