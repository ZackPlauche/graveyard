<template>
  
  <!-- Layout -->
  <div class="min-h-screen grid w-full relative" :class="{ 'grid-cols-3': showCreateForm }">
    
    <!-- Sidebar -->
    <div class="bg-white-500 p-5" v-if="showCreateForm">
      <div>
        <h1 class="text-4xl font-bold">Add Exemplar</h1>
        <ExemplarCreateForm class="bg-white mt-5" @submit="(data) => exemplars.push(data)" />
      </div>
    </div>

    <!-- Exemplars List -->
    <div class="bg-gray-50 p-10 col-span-2 relative w-full overflow-y-auto">
      <header class="flex justify-between items-end">
      <h2>🏆 Exemplars</h2>
        <button @click="showCreateForm = !showCreateForm" class="btn" :class="{ 'bg-red-600 hover:bg-red-500': showCreateForm }">{{ showCreateForm ? 'Cancel' : 'New' }}</button>
      </header>
      <hr class="mt-5">
      <!-- Exemplar Grid -->
      <div class="mt-5 grid grid-cols-3 gap-5">
        <ExemplarCard v-for="exemplar in exemplars" :exemplar="exemplar" />
      </div>
    </div>

  </div>
</template>

<script setup>

const showCreateForm = ref(false)
const { data: exemplars } = await useExemplarModel().list()

</script>
