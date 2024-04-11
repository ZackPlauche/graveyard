<template>
  <ExemplarForm v-bind="$attrs" @submit="updateExemplar" v-model="exemplar" submit-label="Save" />
</template>

<script setup>

const router = useRouter()
const { exemplarId } = defineProps({ exemplarId: Number })
const exemplarModel = useExemplarModel()

const { data: exemplar } = await exemplarModel.get(exemplarId)

const updateExemplar = async (exemplar) => {
  const { status } = await exemparModel.update(exemplarId, exemplar)
  if (status.value === 'success') {
    router.push({ name: 'exemplars-id', params: { id: exemplarId } })
  }
}

</script>