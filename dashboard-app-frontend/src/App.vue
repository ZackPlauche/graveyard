<template>
  <header>
  <Navbar />
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue' 
import { useBlogStore } from '@/stores/blog'
import Navbar from '@/components/Navbar.vue'

const store = useBlogStore()

onMounted(async () => { await store.loadPosts() })


</script>