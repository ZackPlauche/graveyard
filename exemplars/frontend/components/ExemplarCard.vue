<template>
  <NuxtLink :to="{ name: 'exemplars-id', params: { id: exemplar.id }}" class="group bg-white p-5 shadow-md border border-white hover:border-yellow-300 transition-colors text-center relative w-full">
    <!-- Favorite Icon -->
    <div class="absolute top-2.5 right-2 text-3xl cursor-default" title="favorited exemplar" v-if="exemplar.favorite">🏆</div>
    <!-- Exemplar Name -->
    <h3 class="group-hover:text-yellow-900 transition-colors">{{ exemplar.name }}</h3>
    <p class="mt-2 text-gray-600 font-light">{{  exemplar.description }}</p>
    <!-- Exemplar Options -->
    <div class="flex justify-center text-sm gap-2 mt-4 group-hover:opacity-100 opacity-0 transition-all">
      <p class="transition-colors hover:text-cyan-600">View</p>
    </div>
  </NuxtLink>
</template>

<script setup>

const { exemplar } = defineProps({
  exemplar: {
    type: Object,
    required: true,
  }
})

</script>