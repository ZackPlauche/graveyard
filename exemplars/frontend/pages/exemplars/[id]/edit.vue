<template>
  <div class="h-screen grid place-content-center">
    <NuxtLink :to="{ name: 'exemplars-id', params: { id: exemplarId } }" class="btn w-fit">&LeftArrow; Go Back</NuxtLink>
    <h1 class="text-5xl font-bold mt-4">Update Exemplar</h1>
    <ExemplarUpdateForm class="mt-5" :exemplar-id="exemplarId" />
  </div>
</template>

<script setup>
const route = useRoute()
const exemplarId = parseInt(route.params.id)
</script>
