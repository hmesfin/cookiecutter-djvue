import AuthLayout from '@/layouts/AuthLayout.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'

export default [
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: LoginView,
        meta: { requiresGuest: true },
      },
      {
        path: 'register',
        name: 'Register',
        component: RegisterView,
        meta: { requiresGuest: true },
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('./views/ForgotPasswordView.vue'),
        meta: { requiresGuest: true },
      },
      {
        path: 'reset-password/:token',
        name: 'ResetPassword',
        component: () => import('./views/ResetPasswordView.vue'),
        meta: { requiresGuest: true },
      },
    ],
  },
]