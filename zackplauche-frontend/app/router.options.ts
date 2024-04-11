import type { RouterOptions } from '@nuxt/schema'

// https://router.vuejs.org/api/interfaces/routeroptions.html
export default <RouterOptions>{
  linkActiveClass: 'active',
  linkExactActiveClass: 'active-exact',

  scrollBehavior(to, from, savedPosition) {
    // Smooth Scroll to Hash
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      // Scroll to top on each page
      return new Promise((resolve, reject) => {
        setTimeout(() => { resolve({ left: 0, top: 0 }) }, 500) // <- Page transition time taken from fade-in animation in App.vue
      })
    }
  },
}