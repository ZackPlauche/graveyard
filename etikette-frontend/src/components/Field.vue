<template>
    <div class="field">
        <label 
            v-if="label !== null" 
            :for="$attrs.name"
            >{{ label ? label: toLabel($attrs.name) }}</label>
        <component 
            :is="$attrs.type !== 'textarea' ? 'input': 'textarea'"
            v-bind="$attrs" 
            :id="$attrs.id ? $attrs.id: `id_${$attrs.name}`"
            :value="modelValue" 
            @input="$emit('update:modelValue', $event.target.value)"
            >
            <slot></slot>
        </component>
    </div>
</template>

<script>
import { toLabel } from '@/utils/text.js'

export default {
    inheritAttrs: false,
    props: {
        label: { default: '' },
        modelValue: undefined,
    },
    emits: ['update:modelValue'],
    setup() {
        return { toLabel }
    }
}
</script>