<template>
    <BaseButton :class="!editMode ? 'btn-warning' : 'btn-danger'">
        <slot></slot>
    </BaseButton>
</template>

<script>
import BaseButton from './BaseButton.vue'

export default {
    components: {
        BaseButton,
    },
    props: {
        editMode: { type: Boolean, required: true} 
    }
}
</script>