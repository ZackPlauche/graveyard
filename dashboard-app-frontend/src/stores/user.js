import { defineStore } from 'pinia'
import { apiClient } from '@/api/clients'
import { ref, computed, watch } from 'vue'


export const useUserStore = defineStore('user', () => {
  
  const user = ref(null)
  const isAuthenticated = computed(() => Boolean(user.value))

  if (localStorage.getItem('user')) {
    user.value = JSON.parse(localStorage.getItem('user'))
  }

  if (user.value && user.value.token) {
    apiClient.addAuth(user.value.token)
  }

  watch(user, (userVal) => {
    localStorage.setItem('user', JSON.stringify(userVal)) 
  }, { deep: true }
  )


  const login = async (email, password) => {
    let token = await apiClient.post('/api-token-auth/', { username: email, password }).then(data => data.token)
    apiClient.addAuth(token)
    user.value = { token }
    let data = await apiClient.get('/users/current')
    user.value = {...user.value, ...data}
  }

  const logout = () => { 
    user.value = null
    apiClient.clearAuth()
  }

  return { user, login, logout, isAuthenticated }
})