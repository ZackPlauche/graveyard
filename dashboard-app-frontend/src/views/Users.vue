<template>
  <main>
    <ul v-if="users">
      <li v-for="user in users">
        {{ JSON.stringify(user) }}
      </li>
    </ul>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { publicUserModel } from '@/api/models' 

const users = ref(null)
onMounted(async () => { users.value = await publicUserModel.getList() })
</script>