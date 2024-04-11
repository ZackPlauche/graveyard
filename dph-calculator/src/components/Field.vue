<template>
  <div class="w-full">
    <label :for="$attrs.name.toLowerCase()">{{ label ? label : capitalize($attrs.name) }}</label>
    <input v-bind="$attrs"
           :value="modelValue" 
           @input="$emit('update:modelValue', $event.target.value)">
  </div>
</template>

<script setup>

defineProps({
  label: String,
  modelValue: undefined
})
defineEmits(['update:modelValue'])

const capitalize = string => string[0].toUpperCase() + string.slice(1)

</script>

<style scoped>

label {
  @apply block;
}

input {
  @apply p-2 w-full bg-transparent rounded outline-none mt-1.5 transition-shadow
  shadow-[inset_0_0_5px] shadow-black dark:shadow-white
  hover:shadow-sky-400 focus:shadow-sky-400 
  dark:focus:shadow-[sandybrown] dark:hover:shadow-[sandybrown]
  ;
}

</style>