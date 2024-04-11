<template>
    <div class="flex justify-center" :style="{ gap: gap }">
        <slot></slot>
    </div>
</template>


<script>
export default {
    props: { 
        gap: {
            type: String,
            default: '10px', 
        }
    }
}
</script>

