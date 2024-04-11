<template>
  <h2>User List</h2>
  <ul v-if="users.length > 0">
    <li v-for="user in users">{{ user.name }}</li>
  </ul>
  <p v-else>No users yet!</p>
</template>

<script setup>

const { users } = useUsers()

</script>