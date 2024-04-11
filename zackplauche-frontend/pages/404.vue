<template>
  <div class="min-h-screen-navbar grid place-content-center text-center">
    <h1 class="text-8xl text-blue">404 Error</h1>
    <p class="mt-3 text-3xl text-gray-600 font-light">Page Not Found: {{ $route.path }}</p>
    <p class="mt-2"><small>How did you even get here? (👁️👄👁️)</small></p>
    <NuxtLink class="btn bg-blue-dark hover:bg-blue text-white rounded text-2xl px-7 py-3 w-fit mx-auto mt-10" :to="{ name: 'index' }">Go Home 👈(👁️_👁️)</NuxtLink>
  </div>
</template>

<script setup>
useHead({ title: '404'})
</script>