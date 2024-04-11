<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="onSubmit">
      <p><input type="text" placeholder="Email" v-model="formData.email"></p>
      <p><input type="password" placeholder="Password" v-model="formData.password"></p>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const formData = ref({
  email: '',
  password: ''
})

const router = useRouter()
const store = useUserStore()


let onSubmit = async () => {
  let { email, password } = formData.value
  await store.login(email, password)
  if (store.user) {
    router.push({ name: 'Dashboard' })
  }
}

</script>