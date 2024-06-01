import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '../views/LoginView.vue';
import HomeView from '../views/HomeView.vue'
import HomeIncidentsView from '../views/HomeIncidentsView.vue'
import HomeIncidentView from '../views/HomeIncidentView.vue'
import UsersView from '../views/UsersView.vue'

import { useAuthStore } from '@/stores/authStore';

const authGuard = (to, from, next) => {
  const authStore = useAuthStore();

  if (!authStore.isLoggedIn && to.path !== '/login') {
    next('/login');
  } else if (!authStore.isLoggedIn && to.path === '/login') {
    next();
  } else if (to.path === '/login') {
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
      name: 'Home',
      component: HomeView,
      beforeEnter: authGuard,
      children: [
        {
          path: '/',
          name: 'gom',
          component: HomeIncidentsView
        },
        {
          path: '/incident',
          name: 'aa',
          component: HomeIncidentView
        },
        {
          path: '/users',
          name: 'Users',
          component: UsersView
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      beforeEnter: authGuard,
    },
  ],
});

export default router;