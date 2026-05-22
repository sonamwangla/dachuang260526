import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { 
    path: '/visualization', 
    name: 'Visualization', 
    component: () => import('../views/Visualization.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin', 'operator', 'viewer'] }
  },
  { 
    path: '/optimization', 
    name: 'Optimization', 
    component: () => import('../views/Optimization.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin', 'operator'] }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : { role: 'guest' }

  // 1. 登录验证
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  // 2. 角色权限验证
  if (to.meta.allowedRoles) {
    const allowed = to.meta.allowedRoles as string[]
    if (!allowed.includes(user.role)) {
      // 如果权限不足，直接重定向回首页，不使用 alert 阻塞
      return next('/')
    }
  }

  next()
})

export default router
