import { ref, provide, onMounted, watch } from 'vue'


export function useDarkTheme() {

  let initialDarkTheme = localStorage.getItem('darkTheme')
  if (initialDarkTheme) {
    initialDarkTheme = JSON.parse(initialDarkTheme)
  }

  const darkTheme = ref(initialDarkTheme || false)

  onMounted(() => {
    if (localStorage.getItem('darkTheme') === null && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      darkTheme.value = true
    }
  })

  watch(darkTheme, (newDarkTheme) => {
    console.log(newDarkTheme)
    localStorage.setItem('darkTheme', newDarkTheme)
    if (newDarkTheme) {
      document.body.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
    }
  }, { immediate: true })

  provide('darkTheme', darkTheme)

  return { darkTheme }
}