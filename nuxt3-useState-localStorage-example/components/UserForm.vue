<template>
  <h2>User Form</h2>
  <form @submit.prevent="onSubmit">
    <input type="text" v-model="formData.name">
    <button type="submit">Load</button>
  </form>
</template>

<script setup>

const { createUser } = useUsers()

const formData = ref({
  name: '',
})

const onSubmit = () => {
  createUser(Object.assign({}, formData.value))
  formData.value.name = ''
}


</script>