<template>
  <ul class="flex gap-8 snap-x overflow-auto">
    <li class="snap-center first:ml-4" v-for="project in projects">
      <NuxtLink to>
        <ProjectCard :project="project" class="w-[90vw]"></ProjectCard>
      </NuxtLink>
    </li>
  </ul>
</template>

<script setup>
defineProps({
  projects: {
    type: Array[Object],
    required: true,
  }
})
</script>
