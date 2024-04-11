<template>
  <div class="flex flex-col h-screen">
    <Navbar />
    <main class="flex-1">
      <router-view></router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>