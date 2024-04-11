<template>
  <div>
    <h1>Home</h1>
    <h2>To see what I'm trying to accomplish in Nuxt 3...</h2>
    <p>1. Open your developer console and see the global <i>FetchClient</i> object with a "baseURL" key that came from an environment variable in Vite.</p>
    <p>2.<b>That ^ baseURL environment variable piece the main thing I'm trying to replicate in Nuxt.</b></p>
    <p>3. Now go to the <router-link to="/login"><button>Login</button></router-link> page and see that this global FetchClient still has that baseURL AND I was able to have auth headers that persist across pages.</p>
  </div>
</template>

<script setup>
import { useFetchClient } from '@/composables/client.js'

const client = useFetchClient()
console.log(client, client.options.headers)

</script>