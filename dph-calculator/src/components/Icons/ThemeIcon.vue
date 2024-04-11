<template>
  <i :title="darkTheme ? 'Switch to Light Theme' : 'Switch to Dark Theme'"
     class="fas absolute right-0 cursor-pointer text-lg outline-none
            inline-flex items-center justify-center h-10 aspect-square rounded-full 
            transition-colors hover:text-sky-600 dark:hover:text-[sandybrown]
            " 
     :class="darkTheme ? 'fa-sun' : 'fa-moon'" 
     @click="darkTheme = !darkTheme"
     @keypress.enter="darkTheme = !darkTheme"
     @keypress.space="darkTheme = !darkTheme"
     tabindex="0"></i>
</template>

<script setup>
import { inject } from 'vue'

const darkTheme = inject('darkTheme')
</script>