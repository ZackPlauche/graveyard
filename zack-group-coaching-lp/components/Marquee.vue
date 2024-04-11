<template>
  <div class="relative flex overflow-hidden">
      <div class="aspect-square h-24" v-for="icon in icons">
        <img class="h-full w-full object-contain object-center" :src="icon.url" :alt="icon.name + 'Logo'">
      </div>
  </div>
</template>

<script setup lang="ts">
import { icons } from '~/icons'
</script>


<style scoped>

.marquee {
  overflow: hidden;
  white-space: nowrap;
}

.marquee-content {
  display: inline-block;
  animation: marquee 10s linear infinite;
}

@keyframes marquee {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-100%);
  }
}

</style>