<template>
  <div class="flex items-center h-15 justify-between px-6 relative">

    <!-- Navbar Logo -->
    <NuxtLink to="/" class="whitespace-nowrap block text-5xl hover:text-blue transition-colors font-serif md:absolute md:z-20 md:center-x" @click="mobileMenuActive = false">
      Zack Plauché
    </NuxtLink>

    <!-- Link List -->
    <nav class="flex items-center md:hidden">
      <slot></slot>
    </nav>

    <MobileMenuIcon class="absolute right-3 z-20 hidden md:block" v-model="mobileMenuActive" />
    <MobileMenu class="md:grid" :active="mobileMenuActive" @click="mobileMenuActive = false">
      <slot></slot>
    </MobileMenu>

  </div>
</template>

<script setup>
const mobileMenuActive = ref(false)

watch(mobileMenuActive, (status) => {
  if (status) {
    document.body.classList.add('overflow-y-hidden')
  } else {
    document.body.classList.remove('overflow-y-hidden')
  }
})

</script>
