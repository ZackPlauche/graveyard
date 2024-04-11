<template>
  <div class="w-full" :class="attrs.class">
    <label class="block" :for="$attrs.name.toLowerCase()">{{ label ? label : capitalize($attrs.name) }} <span v-if="'required' in $attrs" class="text-red" title="Required">*</span></label>
    <component :is="tagType" class="field" :class="inputClass" ref="input" v-bind="inputAttrs" v-model="value">
      <slot></slot>
    </component>
  </div>
</template>

<script setup>
const props = defineProps({ 
  label: String,
  inputClass: String || Object,
  modelValue: undefined,
})
const emit = defineEmits(['update:modelValue'])

const value = computed({
  get: () => props.modelValue,
  set: (value) => { emit('update:modelValue', value) }
})

const attrs = useAttrs()

const inputAttrs = computed(() => {
  let newAttrs = {}
  for (let attr in attrs) {
    if (attr !== 'class' && attr !== 'style') {
      newAttrs[attr] = attrs[attr]
    }
  }
  return newAttrs
})

const tagType = attrs.type == 'textarea' || attrs.type == 'snippet' ? attrs.type : 'input'

const capitalize = string => string[0].toUpperCase() + string.slice(1)

const input = ref(null)
defineExpose({ input })
</script>

<script>
export default { inheritAttrs: false }
</script>

<style>
.field {
  @apply w-full border p-2 rounded-lg mt-1 outline-none hover:border-cyan focus:border-cyan transition-colors;
}
</style>