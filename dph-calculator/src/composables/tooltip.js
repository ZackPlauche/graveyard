import { ref } from 'vue'

export function useTooltip() {

  const tooltipActive = ref(false)

  function activateTooltip(timeout) {
    tooltipActive.value = true
    setTimeout(() => tooltipActive.value = false, timeout)
  }

  return { tooltipActive, activateTooltip }
}