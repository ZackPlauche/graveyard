<template>
  <div class="flex flex-col min-h-screen bg-white dark:bg-blue-darkest">
    <Navbar>
      <NavLink :to="{ name: 'projects' }" class="hover:text-yellow-400 active-class:text-yellow-400">Projects</NavLink>
      <NavLink :to="{ name: 'about' }" class="hover:text-red active-class:text-red">About</NavLink>
      <NavLink to="/contact" class="hover:text-green active-class:text-green">Contact</NavLink>
    </Navbar>
    <main class="flex-1 min-h-screen-navbar">
      <slot></slot>
    </main>
    <Footer />
  </div>
</template>

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