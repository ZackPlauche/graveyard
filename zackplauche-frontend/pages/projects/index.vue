<template>
  <div class="px-7 py-10 bg-gradient-to-br">
    <div class="mx-auto">
      <div class="text-center">
        <h1 class="font-serif text-8xl text-blue-dark">
          All Projects
        </h1>
        <p class="mt-4">
          Here's a list of all of my active projects. If you happen to come across a particular project that tickles your fancy, you can click on it to learn more!
        </p>
      </div>
      <ProjectGrid class="mt-10" :projects="projects" />
    </div>
  </div>
</template>

<script setup>
const { data: projects } = await useAPIFetch('/projects/?active=true')

useHead({ title: 'Projects' })
</script>