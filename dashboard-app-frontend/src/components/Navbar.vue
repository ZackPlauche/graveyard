<template>
  <div>
    <div v-if="isAuthenticated">
      Welcome, User {{ user.first_name || user.id }}!
    </div>
    <div><router-link :to="{ name: 'Home' }">Dashboard App</router-link></div>
    <nav>
      <ul>
        <li><router-link :to="{ name: 'Blog' }">Blog</router-link></li>
        <li><router-link :to="{ name: 'Images' }">Images</router-link></li>
        <div v-if="!isAuthenticated">
          <li><router-link :to="{ name: 'About' }">About</router-link></li>
          <li><router-link :to="{ name: 'Login' }">Login</router-link></li>
          <li><router-link :to="{ name: 'Register' }">Register</router-link></li>
        </div>
        <div v-else>
          <li><router-link :to="{ name: 'Accounts' }">Accounts</router-link></li>
          <li><router-link :to="{ name: 'Users' }">Users</router-link></li>
          <li><router-link :to="{ name: 'Dashboard' }">Dashboard</router-link></li>
          <li><button @click="logout">Logout</button></li>
        </div>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const store = useUserStore()
const { user, isAuthenticated } =  storeToRefs(store)


const logout = () => {
  store.logout()
  router.push({ name: 'Home' })
}

</script>