<template>
  <!-- Mobile Menu -->
  <div class="fixed inset-0 z-10 bg-white grid place-content-center transition-transform duration-350 ease-in-out" :class="active ? 'translate-x-0' : 'translate-x-full'">
    <div class="flex flex-col text-4xl">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({ active: Boolean })
</script>
