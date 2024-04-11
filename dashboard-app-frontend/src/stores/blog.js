import { ref } from 'vue'
import { defineStore } from 'pinia'
import { blogPostModel } from '@/api/models'


export const useBlogStore = defineStore('blog', () => {
  const posts = ref([])
  const loadPosts = async () => { posts.value = await blogPostModel.getList() }
  return { posts, loadPosts }
})