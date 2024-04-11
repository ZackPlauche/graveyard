
var BASE_URL
if (import.meta.env.DEV) {
  BASE_URL = import.meta.env.BASE_URL + 'api/'
} else {
  BASE_URL = 'https://api.example.com'
}

function fetchClient(BASE_URL) {
  let options = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }
  return {
    get(url, params) {
      url = BASE_URL + url
      if (params) {
        url += new URLSearchParams(params)
      }
      options.method = 'GET'
      return fetch(url, options).then(response => response.json()).catch(error => { console.log('Error: ', error)})
    },
    post(url, data) {
      url = BASE_URL + url
      options.method = 'POST'
      options.body = JSON.stringify(data)
      return fetch(url, options)
              .then(response => response.json())
              .catch(error => { console.log('Error: ', error)})
    }
  }
}


export const client = fetchClient(BASE_URL)

const models = {
  'organization': 'organizations',
}

export function model(model) {
  let url = models[model]
  if (import.meta.env.DEV) {
    url += '.json'
  } else {
    url += '/'
  }
  return {
    get(params) {
      return client.get(url, params)
    }
  }
}