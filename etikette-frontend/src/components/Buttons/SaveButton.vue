<template>
    <BaseButton :class="$attrs.disabled ? 'btn-disabled': 'btn-primary'" >
            <slot>Save</slot>
        </BaseButton>
</template>

<script>
import BaseButton from '@/components/Buttons/BaseButton.vue'

export default {
    components: { BaseButton },
}
</script>