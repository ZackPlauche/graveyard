const apiHost = 'http://127.0.0.1:8000'


export const useAPIFetch = async (endpoint, options) => {
  options = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    ...options
  }
  return await useFetch(`${apiHost}${endpoint}`, options)
}


export const useAPIModel = (endpoint) => {
  
  return {
    get: async (id) => {
      return await useAPIFetch(`${endpoint}${id}/`)
    },
    list: async () => {
      return await useAPIFetch(`${endpoint}`)
    },
    create: async (data) => {
      return await useAPIFetch(`${endpoint}`, {
        method: 'POST',
        body: JSON.stringify(data),
      })
    },
    update: async (id, data) => {
      return await useAPIFetch(`${endpoint}${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data),
      })
    },
    partialUpdate: async (id, data) => {
      return await useAPIFetch(`${endpoint}${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      })
    },
    delete: async (id) => {
      return await useAPIFetch(`${endpoint}${id}/`, {
        method: 'DELETE',
      })
    },
  }
}