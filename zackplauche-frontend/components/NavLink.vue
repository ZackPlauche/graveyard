<template>
  <NuxtLink class="inline-block transition-colors font-extrabold uppercase p-[10px] whitespace-nowrap active-class:text-blue">
    <slot></slot>
  </NuxtLink>
</template>

<script setup>
defineProps({ dropdown: Boolean })
</script>
