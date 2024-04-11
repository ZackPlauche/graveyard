<template>
  <div>

    <!-- Hero Section -->
    <section class="flex min-h-screen-navbar">

      <div class="container px-10 py-10 flex gap-5 flex-row-reverse items-center lg:flex-col sm:px-5">

        <!-- Image -->
        <div class="flex justify-center basis-2/3 lg:basis-0">
          <img src="/zack-pro-dev.jpg" class="rounded-full aspect-square max-w-[500px] lg:max-w-[400px] sm:w-[80%]" alt="">
        </div>

        <!-- Text Content -->
        <div class="lg:text-center">
          <h1 class="font-serif text-blue-dark text-7xl lg:text-6xl sm:leading-tight sm:text-5xl">
            I teach people how to code <span class="whitespace-nowrap"><span class="text-gradient from-orange-400 to-red-500">fast</span><span class="text-6xl sm:text-5xl">🔥</span></span>
          </h1>
          <p class="font-light text-3xl text-gray-700 mt-5 leading-relaxed lg:text-2xl lg:mt-3 ">
            And more. Be sure to take notes.
          </p>

          <!-- Buttons -->
          <div class="flex gap-5 mt-10 text-2xl justify-start lg:justify-center lg:mt-7">
            <a href="https://calendly.com/zackplauche/discovery-call" class="btn bg-blue rounded px-7 py-3" target="_blank">Book a Call <Icon class="fa-solid fa-calendar-check ml-3"></Icon></a>
            <!-- <a class="btn rounded text-blue bg-transparent hover:bg-transparent border border-transparent hover:border-blue">View Offers</a> -->
          </div>
        </div>
      </div>

    </section>

    <!-- Projects Section -->
    <section v-if="projects" class="px-7 py-10 bg-gradient-to-tl bg-gray-100" id="projects">
      <h2 class="font-serif text-7xl text-blue-dark text-center">Featured Projects</h2>
      <ProjectGrid class="mt-10" :projects="projects" />
      <p class="text-center mt-6">
        If you'd like to see more, you can <NuxtLink to="/projects/" class="text-blue hover:underline">view all projects</NuxtLink>.
      </p>
    </section>
  </div>
</template>

<script setup>

const apiHost = 'https://api.zackplauche.com'

const { data: projects } = await useFetch(apiHost + '/projects/?featured=true')
const { data: reviews } = await useFetch(apiHost + '/reviews/')


useHead({ title: 'Zack Plauché | Scale Your Business and Your Life', titleTemplate: String })
</script>


