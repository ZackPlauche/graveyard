<template>
  <ul class="grid grid-cols-3 gap-8 mx-auto max-w-7xl md:grid-cols-1">
    <li v-for="project in projects" :key="project.id">
      <NuxtLink :to="{ name: 'projects-id', params: { id: project.id }}">
        <ProjectCard :project="project"></ProjectCard>
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