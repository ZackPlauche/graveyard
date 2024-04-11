<template>
  <div>
    <form @submit.prevent="onSubmit">
      <h2>Create a New Image</h2>
      <input ref="input" type="file" accept="image/*" />
      <button>Submit</button>
    </form>
    <h1>Images</h1>
    <ul v-if="images">
      <li v-for="image in images" :key="image.id">
        <img :src="image.file || image.url" width="300" alt="" />
      </li>
    </ul>
    <div v-else>No images to show at the moment.</div>
  </div>
</template>

<script setup>
import { imageModel } from '@/api/models'
import { onMounted, ref } from 'vue'


const images = ref(null)
const input = ref(null)


const loadImages = async () => {
  images.value = await imageModel.getList()
}

onMounted(loadImages)

const onSubmit = async () => {
  let formData = new FormData()
  formData.append('file', input.value.files[0])
  let newImage = await imageModel.create(formData)
  console.log(newImage)
  loadImages()
}


</script>