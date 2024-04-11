<template>
  <div class="flex even:flex-row-reverse odd:flex-row items-center mt-6 sm:even:flex-col-reverse sm:odd:flex-col-reverse">
    <div class="p-5 flex-1">
      <img 
        class="block w-full aspect-square object-cover object-center"
        :class="imageClass"
        :src="src"
        :alt="alt"
      />
    </div>
    <div class="flex items-center justify-center flex-1 box-border py-2">
      <div>
        <slot></slot>
      </div>
    </div>
  </div>
</template>


<script setup>
defineProps({
  imageClass: String,
  src: String,
  alt: String,
})
</script>