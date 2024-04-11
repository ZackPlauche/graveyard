<template>
<div class="flex flex-col min-h-screen bg-cover bg-center transition-all bg-[lightgrey] dark:bg-[#0c161c] dark:text-white bg-no-repeat bg-image-random-light dark:bg-image-random-dark">

  <header>
    <Navbar class="py-2 px-4 shadow-md backdrop-blur" />
  </header>

  <main class="flex-1 flex justify-center items-center px-5">
    <Calculator class="shadow-lg bg-white/10 dark:bg-white/5 dark:shadow-black/50" />
  </main>
  <Footer class="backdrop-blur-sm" />
</div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Calculator from '@/components/Calculator.vue'
import { useDarkTheme } from '@/composables/darktheme.js'

useDarkTheme()

</script>