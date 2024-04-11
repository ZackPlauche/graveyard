<template>
<div>

  <section class="shadow">
    <div class="mx-auto max-w-7xl px-2 py-10 sm:py-20">
      <div class="text-center">
        <div class="text-7xl">🌻</div>
      <h1 class="text-5xl sm:text-6xl font-semibold text-neutral-800 mt-16 sm:leading-snug">
        Trustworthy Non-Profits to <br>Help
        <span class="bg-clip-text bg-gradient-to-r from-sky-600 to-yellow-400 text-transparent">Ukraine</span>.
      </h1>
      <p class="text-4xl mt-5 font-light text-neutral-700">Help Ukraine defend against Russian aggression.</p>
      <div class="flex flex-wrap gap-5 justify-center mt-10">
        <router-link class="btn btn-hero bg-sky-500 hover:bg-sky-600 text-white relative flex-1 sm:flex-none" to>
          Help Ukraine Defend Itself
          <span class="absolute inset-x-10 inset-y-2 bg-inherit rounded-full animate-ping hidden sm:inline -z-10 flex-1 sm:flex-none"></span>
        </router-link>
        <router-link class="btn btn-hero bg-yellow-400 text-white" to>Humanitarian Aid</router-link>
      </div>
    </div>
  </div>
</section>

</div>
</template>

<script setup>
import { model } from '@/api/client'
import { onMounted, ref } from 'vue'

const data = ref([])

onMounted(async () => {
  data.value = await model('organization').get()
})

</script>

<style scoped>

.btn {
  @apply inline-flex justify-center items-center whitespace-nowrap
}

.btn-hero { 
  @apply px-10 py-4 text-lg rounded-full transition-colors
}
</style>