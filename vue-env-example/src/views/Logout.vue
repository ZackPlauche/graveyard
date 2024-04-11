<template>
  <div>
    <h1>{{ $route.name }}</h1>
    <h2>You've been logged out!</h2>
    <p><b>Check your developer console (ctrl + shift + i)</b> and see that the auth headers have been add to the global FetchClient! You can visit the 
      <router-link :to="{ name: 'Home' }">Home</router-link> or <router-link :to="{ name: 'About' }">About</router-link> pages and see that the fetch client still has the auth headers.</p>
  </div>
</template>

<script setup>
import { useFetchClient } from '@/composables/client.js'

const client = useFetchClient()
delete client.options.headers.Authorization
console.log(client, client.options.headers)
</script>
