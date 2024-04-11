<!-- <template>
  <section class="pt-10 pb-8 bg-gradient-to-r from-blue-dark to-blue text-white relative lg:py-5 ">
    <header class="container text-center px-5">
      <div class="font-bold text-5xl lg:text-2xl">⭐ 200+ <span class="bg-clip-text text-transparent bg-gradient-to-br from-yellow-300 to-yellow-500">5 Star</span> Reviews ⭐</div>
      <p class="mt-5">See proof on my <a target="_blank" href="https://www.codementor.io/@zackknowspython" class="platform-profile-link" title="Go to Zack's Codementor profile">codementor</a> and <a target="_blank" class="platform-profile-link" href="https://www.wyzant.com/Tutors/LearnPythonWithZack" title="Go to Zack's Wyzant Profile" >Wyzant</a> profiles!</p>
    </header>
    <div class="grid grid-cols-3 gap-5" v-if="showMoreReviews">
      <ReviewCard v-for="(review, index) in reviews" :key="index" :review="review"></ReviewCard>
    </div>
  </section>
</template>

<script setup>
const { data: reviews } = await useFetch('https://api.zackplauche.com/reviews/')


const showMoreReviews = ref(false)
</script>

<style scoped>
.platform-profile-link {
  @apply underline hover:text-yellow-400 transition-colors duration-200 ease-[ease]
}
</style> -->