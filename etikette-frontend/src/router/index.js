import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Pricing from '@/views/Pricing.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Admin from '@/views/Admin'

const routes = [
    { name: 'Home', path: '/', component: Home, meta: { title: 'Home' } },
    { name: 'Pricing', path: '/pricing', component: Pricing, meta: { title: 'Pricing' }, },
    { name: 'Login', path: '/login', component: Login, meta: { title: 'Login' } },
    { name: 'Register', path: '/register', component: Register, meta: { title: 'Sign Up' } },
    { 
        name: 'Admin',
        path: '/admin/', 
        component: Admin.Index,
        redirect: '/admin/dashboard',
        meta: { title: 'Admin'},
        children: [
            { name: 'Dashboard', path: 'dashboard', component: Admin.Dashboard, },
            { name: 'MenuList', path: 'menus/', component: Admin.MenuList, },
            { name: 'MenuAdd', path: 'menus/add', component: Admin.MenuDetail, },
            { name: 'MenuDetail', path: 'menus/:slug', component: Admin.MenuDetail, },
            { name: 'Settings', path: 'settings/', component: Admin.Settings },
        ]
    },
]

const router = createRouter({
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth',
            }
        }
        // Scrolls to top after transition time (milliseconds)
        const transitionTime = 400
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({ left: 0, top: 0})
            }, transitionTime)
        })
    },
    history: createWebHistory(),
    linkActiveClass: 'active',
    linkExactActiveClass: 'active-exact',
    routes,
})

// Set title for each route.
router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | etikette`
    next()
})

export default router