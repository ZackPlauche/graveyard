<template>
  <div>
    <!-- Source: https://tailwindcomponents.com/component/animated-hamburger-menu-icon -->
    <input class="peer absolute inset-0 z-10 opacity-0 cursor-pointer" type="checkbox" v-model="value">
    <button class="relative group">
      <div class="relative flex overflow-hidden items-center justify-center rounded-full w-[50px] h-[50px] transform transition-all ring-0 ring-gray-300 hover:ring-8 group-peer-checked:ring-4 ring-opacity-30 duration-200 shadow-md">
        <div class="flex flex-col justify-between w-[20px] h-[20px] transform transition-all duration-300 origin-center overflow-hidden">
          <div class="bg-black h-[2px] w-7 transform transition-all duration-300 origin-left group-peer-checked:translate-x-10"></div>
          <div class="bg-black h-[2px] w-7 rounded transform transition-all duration-300 group-peer-checked:translate-x-10 delay-75"></div>
          <div class="bg-black h-[2px] w-7 transform transition-all duration-300 origin-left group-peer-checked:translate-x-10 delay-150"></div>

          <div class="absolute items-center justify-between transform transition-all duration-500 top-2.5 -translate-x-10 group-peer-checked:translate-x-0 flex w-0 group-peer-checked:w-12">
            <div class="absolute bg-black h-[2px] w-5 transform transition-all duration-500 rotate-0 delay-300 group-peer-checked:rotate-45"></div>
            <div class="absolute bg-black h-[2px] w-5 transform transition-all duration-500 -rotate-0 delay-300 group-peer-checked:-rotate-45"></div>
          </div>
        </div>
      </div>
    </button>
  </div>
</template>

<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const value = computed({
  get: () => props.modelValue,
  set: (value) => { emit('update:modelValue', value) }
})
</script>