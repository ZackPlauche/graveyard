import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
    { path: '/blog/', name: 'Blog', component: () => import('@/views/Home.vue') },
    { path: '/blog/:id/', name: 'Blog Post', component: () => import('@/views/BlogPost.vue') },
    { path: '/about', name: 'About', component: () => import('@/views/About.vue') },
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue')},
    { path: '/register', name: 'Register', component: () => import('@/views/Register.vue')},
    { path: '/images', name: 'Images', component: () => import('@/views/Images.vue')},
    { path: '/accounts/', name: 'Accounts', component: () => import('@/views/Accounts.vue'), meta: { requiresAuth: true } },
    { path: '/accounts/:id', name: 'Account Detail', component: () => import('@/views/AccountDetail.vue'), meta: { requiresAuth: true } },
    { path: '/users', name: 'Users', component: () => import('@/views/Users.vue'), meta: { requiresAuth: true } },
    { path: '/dashboard/', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta: { requiresAuth: true }},
  ]
})


router.beforeEach((to, from) => {
  // Ensure user is logged in.
  const store = useUserStore()
  const { isAuthenticated } = storeToRefs(store)
  if (!isAuthenticated.value && to.meta.requiresAuth && to.name.toLowerCase() !== 'login') 
    { return { name: 'Login' } 
  }
})

export default router