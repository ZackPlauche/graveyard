<template>
  <div>
    <nav style="display: flex; gap: 10px;">
      <router-link v-for="route in $router.getRoutes()" :to="{ name: route.name }">{{ route.name }}</router-link>
      <a href="https://www.github.com/zackplauche/vue-env-example" target="_blank">Checkout the GitHub Repo</a>
      <a>Built with Vue + Vite</a>
    </nav>
    <RouterView />
  </div>
</template>