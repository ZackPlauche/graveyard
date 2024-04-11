<template>
  <div>
    <h1>About</h1>
  </div>
</template>

<script setup>
import { useFetchClient } from '@/composables/client.js'

const client = useFetchClient()
console.log(client, client.options.headers)

</script>