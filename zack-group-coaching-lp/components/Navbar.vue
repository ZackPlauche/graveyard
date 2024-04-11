<template>
<!-- Navbar -->
<div class="absolute top-0 left-0 right-0 font-serif flex items-center justify-center py-2">
  <NuxtLink class="text-4xl" :to="{ name: 'index' }">{{ title }}</NuxtLink>
</div>
</template>

<script setup lang="ts">

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>
