<template>
  <FormKit :form-class="$attrs.class" :submit-attrs="{ inputClass: 'form-button' }" type="form">
    <div class="space-y-5 p-5">
      <FormKit type="text" name="name" placeholder="Name" validation="required" />
      <FormKit type="textarea" name="description" placeholder="Description" />
      <FormKit type="textarea" name="character" placeholder="Character" help="What character traits do you admire about this exemplar?" />
      <FormKit type="textarea" name="skills" placeholder="Skills" help="What skills does this exemplar have that you'd like to emulate?" />
      <FormKit type="select" name="category" placeholder="Pick a category" :options="categories" />
      <FormKit type="checkbox" name="favorite" wrapper-class="flex gap-2 items-center" input-class="h-5 aspect-square" label-class="-mt-1.5" label="Favorite" />
    </div>
  </FormKit> 
</template>

<script setup>
const categories = ref([])

onMounted(async () => {
  categories.value = await fetch('http://localhost:8000/categories/').then(res => res.json()).then(data => data.map(category => category.name))
  })

</script>

<style>

.formkit-messages {
  @apply mt-1
}

.formkit-message {
  @apply text-sm text-red-500
}

.formkit-help {
  @apply text-sm text-gray-500
}

</style>