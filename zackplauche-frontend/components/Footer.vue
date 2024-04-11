<template>
  <footer class="bg-white-100 border-t">

    <!-- Grid -->
    <div class="grid gap-y-10 grid-cols-3 max-w-7xl divide-x-2 py-10 mx-auto lg:gap-y-20 lg:py-20 lg:grid-cols-1">

      <!-- Logo -->
      <div class="flex flex-col justify-center items-center font-serif text-5xl text-blue h-full">
          <div>Zack Plauché</div>

          <!-- Social Icons -->
          <div class="flex gap-3 items-center">
            <a href="https://www.youtube.com/channel/UCPsi8tNv7UuNRljOTK5sl4A" title="Subscribe to my YouTube channel" target="_blank">
              <Icon class="footer-icon fa-brands fa-youtube"></Icon>
            </a>
            <a href="https://discord.gg/qA2jRybdRy" title="Join my Discord, for degens (^-^🌸)" target="_blank">
              <Icon class="footer-icon fa-brands fa-discord"></Icon>
            </a>
            <a href="https://github.com/ZackPlauche" title="Get Gitty over my Github Projects" target="_blank">
              <Icon class="footer-icon fa-brands fa-github"></Icon>
            </a>
            <a href="https://www.facebook.com/ZackPlauche" title="Follow me on Facebook" target="_blank">
              <Icon class="footer-icon fa-brands fa-facebook-f"></Icon>
            </a>
            <a href="https://www.instagram.com/zackplauche" title="Follow me on Instagram" target="_blank">
              <Icon class="footer-icon fa-brands fa-instagram"></Icon>
            </a>
          </div>
        </div>

        <!-- Links -->
        <div class="flex items-center justify-center">
          <nav class="grid grid-cols-2 gap-x-10">
            <NavLink class="hover:text-blue" to="/">Home</NavLink>
            <NavLink class="hover:text-blue" to="/contact">Contact</NavLink>
            <NavLink class="hover:text-blue" to="/projects/">Projects</NavLink>
            <NavLink class="hover:text-blue" to="/about">About</NavLink>
          </nav>
        </div>

        <!-- Discord Footer Call to Action -->
        <div class="text-center px-5">
          <h4 class="font-serif text-4xl text-discord-gray lg:text-5xl">Join My Discord.</h4>
          <p class="text-sm mt-2 lg:mt-3">Get access to my exclusive content and a community of passionate developers to take you to the next level.</p>
          <a class="btn group bg-discord-gray rounded-md px-3 text-white mt-5 hover:bg-discord lg:px-4 lg:bg-discord lg:hover:bg-discord/80 "
             href="https://discord.gg/qA2jRybdRy" target="_blank">
            <Icon class="fa-brands fa-discord"></Icon>
            <span class="ml-3 text-sm lg:text-base">Join My Server</span>
          </a>
        </div>

    </div>

    <!-- Copyright -->
    <div class="text-center py-2 bg-blue text-white">&copy; Zack Plauche LLC 2022</div>

  </footer>
</template>

<style>

  .footer-icon {
    @apply text-xl h-10 rounded-full 
    transition-colors bg-blue-dark text-white hover:bg-blue
  }
</style>