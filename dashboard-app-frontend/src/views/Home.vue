<template>
<main>
  <h1>Blog</h1>
  <ul>
    <li v-for="post in store.posts" :key="post.id">
      <router-link :to="{ name: 'Blog Post', params: { id: post.id }}">
        <h2>{{ post.title }}</h2>
      </router-link>
    </li>
  </ul>

</main>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useBlogStore } from '@/stores/blog'

const store = useBlogStore()
</script>
