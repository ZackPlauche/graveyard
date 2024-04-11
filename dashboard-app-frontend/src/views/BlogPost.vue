<template>
  <main>
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
  </main>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useBlogStore } from '@/stores/blog'

const route = useRoute()
const store = useBlogStore()
let post = store.posts.find(post => post.id == route.params.id)
</script>