<template>
  <div>
    <div>
      <h1>Public Accounts</h1>
      <ul>
        <li v-for="account in accounts">
          <router-link :to="{ name: 'Account Detail', params: { id: account.id }}">{{ account.id }}</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { publicUserModel } from '@/api/models'
import { onMounted, ref } from 'vue'

const accounts = ref(null)

onMounted(async () => {
  accounts.value = await publicUserModel.getList()
})

</script>