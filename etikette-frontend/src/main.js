import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import Field from '@/components/Field.vue'
import Hero from '@/components/Hero.vue'

const app = createApp(App)

app.component('field', Field)
app.component('hero', Hero)

app.use(router).mount('#app')