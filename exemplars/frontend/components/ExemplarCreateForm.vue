<template>
  <ExemplarForm id="exemplarCreateForm" @submit="createExemplar" submit-label="Create Exemplar" />
</template>

<script setup>
import { reset } from '@formkit/core'


const emits = defineEmits(['submit'])


const createExemplar = async (exemplarData) => {
  const { data: newExemplar, status } = await useExemplarModel().create(exemplarData)
  if (status.value === 'success') {
    reset('exemplarCreateForm')
    emits('submit', newExemplar.value)
  }
}

</script>