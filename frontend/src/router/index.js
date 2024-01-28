import { createRouter, createWebHistory } from 'vue-router'

import LoginMainView from '../views/LoginMainView.vue'
import AdminMainView from '../views/AdminMainView.vue'
import ChatView from '../views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginMainView
    },
    {
      path: '/',
      name: 'Admin',
      component: AdminMainView
    },
    {
      path: '/chat',
      name: 'Chat',
      component: ChatView
    },

  ]
})

export default router
