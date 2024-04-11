<template>
    <!-- Tooltip -->
    <Transition>
      <div v-if="active" class="rounded-lg p-2 text-sm absolute left-1/2 -translate-x-1/2 -translate-y-full bg-black/80 text-white dark:bg-white/90 dark:text-black">
        <slot></slot>
      </div>
    </Transition>
</template>

<script setup>
defineProps({ active: Boolean })
</script>

<style scoped>

.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

</style>