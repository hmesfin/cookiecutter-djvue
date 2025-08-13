import MainLayout from '@/layouts/MainLayout.vue'
import HomeView from './views/HomeView.vue'

export default [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: HomeView,
      },
      {
        path: 'features',
        name: 'Features',
        component: () => import('./views/FeaturesView.vue'),
      },
      {
        path: 'pricing',
        name: 'Pricing',
        component: () => import('./views/PricingView.vue'),
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('./views/AboutView.vue'),
      },
      {
        path: 'contact',
        name: 'Contact',
        component: () => import('./views/ContactView.vue'),
      },
    ],
  },
]