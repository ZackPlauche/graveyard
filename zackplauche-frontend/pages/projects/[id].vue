<template>
  <div class="relative">

    <!-- Project Detail Header -->
    <div
      v-if="project.thumbnail"
      class=" bg-cover bg-center bg-blend-multiply bg-black/60 bg-fixed px-5"
      :style="{ 'background-image': `url('${project.thumbnail.file || project.thumbnail.url}')` }"
    >
      <div class="mx-auto max-w-7xl text-center relative flex justify-center items-center min-h-screen-navbar py-10">

        <NuxtLink 
          class="absolute left-0 top-[1.875rem] hover:-translate-x-2 transition-transform"
          title="Go back"
          :to="{ name: 'projects' }"
        >
          <Icon class="fa-solid fa-left-long h-14 bg-white transition-colors rounded-full hover:text-cyan-500 text-blue-dark text-2xl"></Icon>
        </NuxtLink>

        <div>

          <h1 class="text-white text-8xl font-serif text-center sm:text-7xl">{{ project.title }}</h1>
          <p class="mt-2 text-2xl t-gray-700 text-white sm:mt-5">{{ project.shortDescription }}</p>
          <div class="mt-10 flex justify-center gap-3">
            <a v-if="project.siteUrl" :href="project.siteUrl" target="_blank" title="Visit Project Website">
              <Icon class="fas fa-external-link-alt project-detail-icon text-lg text-white bg-blue-dark hover:bg-blue"></Icon>
            </a>
            <a v-if="project.githubUrl" :href="project.githubUrl" target="_blank">
              <Icon class="fa-brands fa-github project-detail-icon text-2xl text-white bg-black hover:bg-white hover:text-black"></Icon>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>


<script setup>
const route = useRoute()
const { data: project } = await useAPIFetch(`/projects/${route.params.id}`)

useHead({ title: project.value.title })
</script>

<style scoped>

.project-detail-icon {
  @apply rounded-full h-14 transition-colors
}

</style>