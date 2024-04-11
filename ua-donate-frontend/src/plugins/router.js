import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {path: '', name: 'home', component: () => import('@/views/Home.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
  linkActiveClass: 'active',
  linkExactActiveClass: 'active-exact'
})


// Make router change the page title
router.afterEach((to, from) => {
  document.title = to.meta.title || 'UA Donate'
})

export default router