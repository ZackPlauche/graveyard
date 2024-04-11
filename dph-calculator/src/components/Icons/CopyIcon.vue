<template>
  <div class="aspect-square inline-flex items-center justify-center relative cursor-pointer">

    <Tooltip class="cursor-default" :active="tooltipActive">Copied to clipboard!</Tooltip>

    <i class="fas fa-copy" 
      @click="copyToClipboard(value); activateTooltip(2000)"
      @keypress.enter="copyToClipboard(value); activateTooltip(2000)"
      title="Copy result">
    </i>
  </div>
</template>

<script setup>
import Tooltip from '@/components/Tooltip.vue'
import { useTooltip } from '@/composables/tooltip.js'

const { tooltipActive, activateTooltip } = useTooltip()

defineProps({ value: { type: undefined, required: true } })

const copyToClipboard = value => navigator.clipboard.writeText(value)
</script>
