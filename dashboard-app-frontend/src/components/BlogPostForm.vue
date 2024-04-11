<template>
<form @submit.prevent="onSubmit">
  <slot name="header">
  <header>
    <h2>Create a New Blog Post</h2>
  </header>
  </slot>
  <p><input v-model="formData.title" type="text" name="title" placeholder="Post Title"></p>
  <p><textarea v-model="formData.body" name="" id="" cols="30" rows="10" placeholder="Body"></textarea></p>
  <button type="submit">Submit</button>
</form>
</template>

<script setup>
import { ref } from 'vue'
import { useBlogStore } from '@/stores/blog'
import { apiClient } from '@/api/clients'
import { blogPostModel } from '@/api/models'


const blogStore = useBlogStore()

const formData = ref({
  title: '',
  body: '',
})

const onSubmit = async () => {
  console.log(apiClient.options.headers)
  await blogPostModel.create(formData.value)
  blogStore.loadPosts()
}
</script>