<template>
  <div class="group bg-white h-60 relative overflow-hidden rounded-2xl">
    <img class="object-cover object-center h-full w-full group-hover:scale-[1.14] transition-transform duration-400 will-change-transform" :src="project.thumbnail.file || project.thumbnail.url" :alt="project.thumbnail.alt">
    <div class="px-5 py-4 transition absolute inset-0 bg-black/30 group-hover:bg-black/60 flex items-center justify-center">
      <h3 class="text-3xl font-bold text-white text-center">{{ project.title }}</h3>
    </div>
    <div class="absolute text-white opacity-0 group-hover:opacity-100 transition-opacity center-x transform bottom-10 text-lg">Learn More</div>
  </div>
</template>

<script setup>
defineProps({ project: { type: Object, required: true } })
</script>
