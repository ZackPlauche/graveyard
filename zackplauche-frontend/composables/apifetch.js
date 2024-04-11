

export const useAPIFetch = (resourcePath, options) => {
  const config = useRuntimeConfig()
  options = {
    key: resourcePath,
    baseURL: config.public.apiUrl,
    headers: {
      'Accept': 'application/json',
    },
    ...options
  }
  return useFetch(resourcePath, options)
}
