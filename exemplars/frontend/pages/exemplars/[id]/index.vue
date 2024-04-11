<template>
  <div class="p-5">
    <div class="container">
      <NuxtLink :to="{ name: 'index' }" class="btn">&LeftArrow; Go Back</NuxtLink>
      <div v-if="exemplar" class="mt-5">
        <h1 class="text-5xl font-bold font-serif">{{ exemplar.name }}<span v-if="exemplar.favorite">🏆</span></h1>
        <div class="space-y-5">
          <p class="whitespace-pre-wrap text-2xl font-light">{{ exemplar.description }}</p>
          <div v-if="exemplar.character">
            <h2 class="">Character</h2>
            <p class="whitespace-pre-wrap">{{ exemplar.character }}</p>
          </div>
          <div v-if="exemplar.skills">
            <h2>Skills</h2>
            <p class="whitespace-pre-wrap">{{ exemplar.skills }}</p>
          </div>
          <!-- Control Buttons -->
          <div class="mt-5 flex gap-2">
            <NuxtLink :to="{ name: 'exemplars-id-edit', params: { id: exemplar.id } }" class="btn">Edit</NuxtLink>
            <button @click="handleDelete(exemplar)" class="btn bg-red-800 hover:bg-red-700">Delete</button>
            <button @click="toggleFavorite(exemplar)" class="btn bg-amber-600 hover:bg-amber-500">Toggle Favorite</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

const router = useRouter()
const route = useRoute()

const exemplarModel = useExemplarModel()
const { data: exemplar } = await exemplarModel.get(route.params.id)

if (!exemplar.value) {
  router.push({ name: 'index' })
}

const handleDelete = async (exemplar) => {
  const { status } = await exemplarModel.delete(exemplar.id)
  if (status.value === 'success') {
    router.push({ name: 'index' })
  }
}
  
const toggleFavorite = async (exemplar) => {
  exemplar.favorite = !exemplar.favorite
  await exemplarModel.update(exemplar.id, exemplar)
}

</script>