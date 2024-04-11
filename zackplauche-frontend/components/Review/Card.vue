<template>
  <div class="bg-white rounded-2xl max-w-2xl text-gray-700 relative mx-auto text-center shadow-lg grid overflow-hidden">
    <div class="p-5 py-10">
      <p>{{ review.text }}</p>
      <div class="mt-3">~ <span class="font-bold">{{ review.clientFirstName }} {{ review.clientLastName }}</span></div>
    </div>
  </div>
</template>

<script setup>
defineProps({ review: Object })
</script>