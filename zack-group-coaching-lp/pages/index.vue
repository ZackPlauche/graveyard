<template>
  <div>
    <section class="bg-neutral-900 min-h-screen text-white flex items-center px-20 lg:px-5 relative lg:py-[56px] lg:pb-10">
      
      <Navbar title="Zack Plauché"/>

      <!-- Main Content -->
      <div class="mx-auto w-full max-w-screen-2xl grid grid-cols-10 lg:flex flex-col-reverse">
        
        <!-- Text and CTA -->
        <div class="col-span-5 flex items-center lg:mt-7">
          <div class="lg:text-center">
            <h1 class="font-bold text-7xl lg:text-5xl">Group Courses</h1>
            <p class="text-2xl mt-4 sm:text-lg sm:leading-6">Learn to code from a seasoned developer AND code mentor <b class="bg-clip-text text-transparent bg-gradient-to-t from-cyan-300 to-green-400">that knows how to teach!</b></p>
            <p class="mt-3 text-lg sm:hidden"><span class="sm:hidden">The </span><span class="capitalize">same</span> great training, fraction of the price.</p>
            <div class="mt-5 leading-tight">
              <div class="font-bold line-through text-6xl text-red-500 lg:hidden">${{ oneOnOneRate }} for 1 hour</div>
              <div class="font-bold line-through text-5xl text-red-500 hidden lg:block">${{ oneOnOneRate }}/hour</div>
              <div class="font-bold text-green-500 text-5xl mt-3 lg:hidden">${{ groupLessonRate }}/lesson for {{ groupLessonAmount }} lessons (${{ coursePrice }} total)</div>
              <div class="font-bold text-green-500 text-3xl mt-3 hidden lg:block">${{ groupLessonRate }}/lesson for 24 lessons (${{ coursePrice }} total)</div>
              <p class="text-sm mt-4">Pay over time with <img src="/images/logos/afterpay/blackmint.png" class="inline-block h-[20px] mb-.5" /> as low as $54/month!</p>
            </div>
            <a :href="stripePaymentLink" target="_blank" class="button text-2xl mt-10 px-10 py-5 transition-all duration-200 ease-[ease] hover:bg-blue-400 shadow-xl">Enroll Now</a>
            <p class="text-sm mt-2">Checkout provided by <img class="inline-block h-[32px] mb-0.5 -ml-1.5 -mr-1" src="/images/logos/stripe-logo.png" /></p>
          </div>
        </div>

        <!-- Image -->
        <div class="aspect-square rounded-full overflow-hidden col-span-5 w-5/6 place-self-end lg:place-self-center lg:mt-2 lg:max-w-[400px]">
          <img 
            src="/images/zack/moldova-pro-photo-rectangle.jpg" 
            alt="Zack Plauché looking professional and cool staring into your beautiful soul." 
            class="object-[-40px] object-cover w-full h-full" />
        </div>

      </div>

</section>
</div>
</template>

<script setup>


const oneOnOneRate = ref(250)
const groupLessonRate = ref(35)
const groupLessonAmount = ref(24)

const coursePrice = computed(() => {
  return groupLessonRate.value * groupLessonAmount.value
})

const stripePaymentLink = 'https://buy.stripe.com/dR6dS9fgZfCpbdueUU'


</script>