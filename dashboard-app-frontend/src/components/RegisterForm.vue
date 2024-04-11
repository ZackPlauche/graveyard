<template>
<form @submit.prevent="onSubmit">
  <slot name="header">
  <header>
    <h2>Register Here</h2>
  </header>
  </slot>
  <p><input v-model="form.data.email" type="email" name="email" placeholder="Email"></p>
  <p><input v-model="form.data.firstName" type="text" name="firstName" placeholder="First name"></p>
  <p><input v-model="form.data.lastName" type="text" name="lastName" placeholder="Last name"></p>
  <p><input v-model="form.data.password" type="password" name="password" placeholder="Password"></p>
  <p><input v-model="form.data.password2" type="password" name="password2" placeholder="Confirm your password"></p>
  <div>{{ passwordsMatch }}</div>
  <div>{{ form.data.email }} {{ form.data.firstName }}</div>
  <button type="submit">Submit</button>
</form>
</template>

<script setup>
import { watch, ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { apiClient } from '@/api/clients'
import { useRouter } from 'vue-router'


const router = useRouter()

const form = ref({
  data: {
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    password2: '',
  },
  errors: [],
})

const store = useUserStore()

const passwordsMatch = computed(() => {
  const { password, password2 } = form.value.data 
  return password === password2
})


const onSubmit = async () => {
  const { email, firstName, lastName, password } = form.value.data
  
  // If Successful
  if (passwordsMatch.value) {
    console.log(email)
    let data = {
      email,
      'first_name': firstName,
      'last_name': lastName,
      password
    }
    let newUser = await apiClient.post('/users/', data)
    await store.login(newUser.email, password)
    router.push({ name: 'Dashboard' })
  }

}
</script>