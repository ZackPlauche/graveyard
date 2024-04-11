<template>
  <form class="mx-auto max-w-screen-sm backdrop-blur px-5 pt-7 pb-4 rounded-2xl w-full">
    <div class="flex gap-4">
      <Field min="0" type="number" name="hours" v-model="hours" />
      <Field min="0" type="number" name="minutes" v-model="minutes" />
      <Field min="0" type="number" name="seconds" v-model="seconds" />
    </div>
    <Field min="0" class="mt-3" type="number" name="hourlyRate" label="Hourly Rate" v-model="hourlyRate" />
    <hr class="border-black dark:border-white transition-colors mt-5">
    <div class="mt-5 flex justify-between">
      <div class="text-4xl">Result: <span :class="{ 'text-green-600 dark:text-green-400': result > 0 }">$<span>{{  result  }}</span></span></div>
      <CopyIcon class="text-3xl outline-black dark:outline-white transition-all hover:text-sky-500 dark:hover:text-[sandybrown]" :class="result > 0 ? 'opacity-1': 'opacity-0'" :value="result" />
    </div>
  </form>
</template>

<script setup>
import { ref, computed, watch, onMounted} from 'vue'
import Field from '@/components/Field.vue';
import CopyIcon from '@/components/Icons/CopyIcon.vue'

const initialHourlyRate = localStorage.getItem('hourlyRate')

const hours = ref(0)
const minutes = ref(0)
const seconds = ref(0)
const hourlyRate = ref(initialHourlyRate || 0.00)

watch(hourlyRate, (newHourlyRate) => {
  if (newHourlyRate > 0) {
    localStorage.setItem('hourlyRate', newHourlyRate)
    console.info('hourlyRate added.')
  } else {
    localStorage.removeItem('hourlyRate')
    console.info('hourlyRate removed.')
  }
})

const result = computed(() => {
  let totalTimeInSeconds = (hours.value * 3600) + (minutes.value * 60) + seconds.value
  let dollarsPerSecond = hourlyRate.value / 3600
  let result = (totalTimeInSeconds * dollarsPerSecond).toFixed(2)
  return result 
})

</script>