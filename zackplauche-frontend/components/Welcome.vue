<template>
  <div class="flex flex-col h-screen-navbar max-h-[693.6px]">
    <div class="flex items-center box-border pb-2 sm:py-2">
      <div class="container mx-auto px-2 text-blue-dark text-center py-3">
        <h1 class="font-serif text-4xl sm:text-5xl md:text-6xl tracking-tight">
          <span class="tracking-tightest">W</span>elcome to
          <span class="text-blue hidden sm:inline">ZackPlauche.com</span>
          <span class="text-blue sm:hidden">my site</span>!
        </h1>
        <div class="group w-fit mx-auto relative mt-4">
          <img
            class="inline-block h-80 aspect-square object-cover object-center rounded-full"
            src="/zack-sozopal.jpg"
            alt="Zack smiling in front of Sozopal beachfront."
          />
          <p class="absolute hidden md:block -right-3/4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity xl:text-lg">
            You'll see me a lot here... ;)
          </p>
        </div>
        <p class="text-2xl md:text-3xl lg:text-4xl font-normal mt-4">What brings you here?</p>
      </div>
    </div>
    <div class="grid grid-rows-4 flex-1">
      <div class="grid lg:grid-cols-3 row-start-1 row-end-4">
        <a class="contents" href="https://www.codementor.io/@zackknowspython" target="_blank">
          <OptionBlock class="bg-blue-darkest hover:bg-black text-white hover:text-cyan">
            <span>I want to <span class="text-cyan">Build a Project</span>. 👨‍💻</span>
          </OptionBlock>
        </a>
        <a class="contents" href="https://www.codementor.io/@zackknowspython" target="_blank">
          <OptionBlock class="bg-blue-darkest hover:bg-black text-white hover:text-cyan">
            I want to <span class="text-cyan">Learn From You</span>. 🧠
          </OptionBlock>
        </a>
        <a class="contents" :href="`mailto:${email}`" target="_blank">
          <OptionBlock class="bg-blue-darkest hover:bg-black text-white hover:text-cyan">
            I wish to <span class="text-cyan">Collaborate</span>. 🎨
          </OptionBlock>
        </a>
      </div>
      <NuxtLink to="/#about" class="contents">
        <OptionBlock class="group row-start-4 row-end-5 text-blue-dark hover:text-blue">
          I want to learn <span class="text-blue">About You</span>. 🙂
        </OptionBlock>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import OptionBlock from '@/components/OptionBlock.vue'

const email = 'zackknowspython@gmail.com'

</script>