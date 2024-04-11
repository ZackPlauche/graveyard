<template>
  <div class="px-7 py-10 bg-gradient-to-br">
    <div class="mx-auto">
      <header class="text-center">
        <h1 class="font-serif text-8xl text-blue-dark">
          Offers
        </h1>
        <p class="mx-auto max-w-2xl">Checkout my latest products and services! I frequently expand my product and service selection to best provide value to my customers 🙂.</p>
      </header>

      <!-- Offer Card List-->
      <ul class="grid grid-cols-3 gap-8 mx-auto max-w-7xl mt-10 md:grid-cols-1" v-if="offers">

        <li v-for="offer in offers" :key="offer.id">
          <NuxtLink :to="offer.actionUrl">
            <div
              class="shadow-[0_0_10px_lightgray] hover:shadow-[0_0_10px] hover:shadow-blue transition-all cursor-pointer rounded-3xl px-5 py-5 text-center h-full"
              :style="{ boxShadow: `0 0 10px ${offer.color}` }">
              <img v-if="offer.icon" :src="offer.icon.file || offer.icon.url" class="w-20 mx-auto" alt="">
              <h3 class="font-bold text-3xl mt-4 text-blue-dark">{{ offer.title }}</h3>
              <p class="mt-5" v-if="offer.description">{{ offer.description }}</p>
              <!-- <a v-if="offer.callToAction" class="btn rounded-md mt-10">{{ offer.callToAction }}</a> -->
            </div>
          </NuxtLink>
        </li>

      </ul>

    </div>
  </div>
</template>

<script setup>
const { data: offers } = await useAPIFetch('/offers/')

console.log(offers.value)

useHead({ title: 'Offers' })
</script>