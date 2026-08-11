import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      redirect: '/login'
    },

    {
      path: '/login',
      component: Login
    },

    {
      path: '/register',
      component: Register
    },

    {
      path: '/home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },

    {
      path: '/oauth/callback',
      name: 'OAuthCallback',
      component: () => import('@/views/OAuthCallback.vue')
    }
  ]
})

// router.beforeEach((to) => {
//   if (to.meta.requiresAuth && !localStorage.getItem('token')) {
//     return '/home'
//   }
// })

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  // 需要登录 且 无token → 去首页
  if (to.meta.requiresAuth && !token) {
    return '/login'
  }
  // 其他情况正常放行
  return true
})

export default router
