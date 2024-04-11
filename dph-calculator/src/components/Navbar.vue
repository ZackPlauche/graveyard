<template>

  <div class="py-2 px-4 shadow-md backdrop-blur dark:bg-black/30">
      <div class="h-15 relative mx-auto max-w-7xl flex items-center">

        <!-- Navbar Logo -->
        <div class="absolute center text-5xl font-thin whitespace-nowrap">
          <span class="text-sky-600 dark:text-[sandybrown]"> <!-- Add Color Here -->
            <span class="hidden sm:inline">DollarPerHour</span>
            <span class="sm:hidden">DPH</span>
          </span> 
          Calc<span class="hidden sm:inline">ulator</span>
        </div>

        <ThemeIcon class="tap-highlight-none" />
      </div>
  </div>
</template>

<script setup>
import ThemeIcon from '@/components/Icons/ThemeIcon.vue'
</script>