import { createRouter, createWebHistory } from 'vue-router'

import LoginMainView from '../views/LoginMainView.vue'

import AdminMainView from '@/views/AdminMainView.vue'
import AdminShiftsChildView from '@/views/AdminShiftsChildView.vue'
import AdminUsersChildView from '@/views/AdminUsersChildView.vue'
import ChatView from '../views/ChatView.vue'

import { useAuthStore } from '@/stores/authStore';

const authGuard = (to, from, next) => {
  const authStore = useAuthStore();

  if (!authStore.isLoggedIn && to.path != '/login') {
    next('/login');
  } else if (!authStore.isLoggedIn && to.path == '/login') {
    next();
  } else if (to.path == '/login') {
    next('/');
  } else {
    next();
  }
};
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Chat',
      component: ChatView,
      beforeEnter: authGuard
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminMainView,
      beforeEnter: authGuard,
      children: [
        { path: 'shifts', name: 'AdminShifts', component: AdminShiftsChildView },
        { path: 'users', name: 'AdminUsers', component: AdminUsersChildView },
      ],
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginMainView,
      beforeEnter: authGuard
    },
  ]
})

export default router
