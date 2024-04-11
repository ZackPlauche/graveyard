<template>
  <!-- Google Tag Manager (noscript) -->
  <noscript>
    <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KXQVQRCW" height="0" width="0" style="display:none;visibility:hidden"></iframe>
  </noscript>
  <!-- End Google Tag Manager (noscript) -->
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>

useHead({
  titleTemplate: title => title ? `${title} | Zack Plauché` : 'Page | Zack Plauché',
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  @apply transition-opacity duration-500
}

.fade-enter-from,
.fade-leave-to {
  @apply opacity-0
}
</style>