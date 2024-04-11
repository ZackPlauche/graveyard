


class FetchClient {
  defaultOptions = { headers: { 'Accept': 'application/json' }}

  constructor(baseURL, options) {
    this.baseURL = baseURL
    this.options = {...this.defaultOptions, ...options}
  }

  get(url) { return fetch(this.baseURL + url, this.options).then(response => response.json()).catch(error => console.error(error)) }
}

const client = new FetchClient(import.meta.env.VITE_API_URL)

export const useFetchClient = () => {
  return client
}