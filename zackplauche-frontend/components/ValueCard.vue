<template>
  <div class="bg-white text-center border aspect-square w-fit p-4 flex rounded-xl max-w-[240px] transition-all duration-300 ease-[ease] hover:scale-[1.1] will-change-transform cursor-default hover:border-cyan-400">
    <div>
      <!-- Emoji -->
      <div class="text-5xl">{{ value.emoji }}</div>
      <h4 class="bentham text-2xl mt-2">{{ value.name }}</h4>
      <p class="text-sm mt-1.5">{{ value.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">

// define an object called Value
interface Value {
  emoji: string;
  name: string;
  description: string;
}


defineProps<{
  value: Value;
}>();
</script>