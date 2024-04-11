

const addSearchParams = (url, params) => {
  url = new URL(url)
  params = new URLSearchParams({...url.searchParams, ...params})
  url.search = params.toString()
  return url
}

const handleResponse = response => {
  if (response.ok) { return response.json() }
  throw new Error(response.message)
}
const handleError = (error) => { console.error(error); alert(error)}


class FetchClient {
  defaultHeaders = {
    'Accept': 'application/json'
  }

  constructor(baseURL, options) {
    this.baseURL = baseURL
    this.options = { headers: this.defaultHeaders, ...options }
  }

  get(url, params) {
    if (params) {
      url = addSearchParams(url, params)
    }
    return fetch(this.baseURL + url, this.options).then(handleResponse).catch(handleError)
  }

  post(url, data) {
    return fetch(this.baseURL + url, {method: 'POST', body: this.#handleData(data), ...this.options}).then(handleResponse).catch(handleError)
  }

  put(url, data) {
    return fetch(this.baseURL + url, {method: 'PUT', body: this.#handleData(data), ...this.options}).then(handleResponse).catch(handleError)
  }

  patch(url, data) {
    return fetch(this.baseURL + url, {method: 'PATCH', body: this.#handleData(data), ...this.options}).then(handleResponse).catch(handleError)
  }

  delete(url) {
    return fetch(this.baseURL + url, { method: 'DELETE', ...this.options}).catch(handleError)
  }

  addAuth(token) {
    this.options.headers.Authorization = `Token ${token}`
  }

  clearAuth() {
    if (this.options.headers.Authorization) {
      delete this.options.headers.Authorization
    }
  }

  /**
   * Handle data and content-type of incoming data for handling image uploads.
   * @param {*} data 
   * @returns 
   */
  #handleData(data) {
    if (data instanceof FormData) {
      delete this.options.headers['Content-Type']
      return data
    } else {
      this.options.headers['Content-Type'] = 'application/json'
      return JSON.stringify(data)
    }
  }
}


export const apiClient = new FetchClient('http://localhost:8000')