<template>
  <main>
    <div v-if="user">
      <h1>User {{ user.id }}</h1>
      <h2>Manage Posts</h2>
      <ul>
        <li v-for="post in posts" :key="post.id">
          {{ post.title }}
          <button v-if="post.author === userStore.user.id" @click="deletePost(post.id)">Delete</button>
        </li>
      </ul>
    </div>
  </main>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { publicUserModel, blogPostModel } from '@/api/models'
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user'
import { useBlogStore } from '@/stores/blog'

const route = useRoute()
const user = ref(null)
const posts = ref(null)
const userStore = useUserStore()
const blogStore = useBlogStore()


const loadUser = async () => {
  user.value = await publicUserModel.get(route.params.id)
  posts.value = user.value.posts
}

onMounted(loadUser)

const deletePost = async (postID) => {
  await blogPostModel.delete(postID)
  posts.value = posts.value.filter(post => post.id !== postID)
  blogStore.loadPosts()
}

</script>
