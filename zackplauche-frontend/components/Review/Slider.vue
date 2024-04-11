<template>
  <ul class="flex snap-x pb-5 overflow-x-auto py-10 scrollbar" v-if="reviews">
    <li v-for="review in reviews" class="min-w-[100vw] snap-center">
      <ReviewCard :review="review" />
    </li>
  </ul>
</template>

<script setup>

interface 

defineProps({
  reviews: { type: Array, required: true }
})
</script>
