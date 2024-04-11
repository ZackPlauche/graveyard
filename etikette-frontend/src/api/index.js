import axios from 'axios'

const baseDomain = 'http://127.0.0.1:8000'
const token = '9f071c54d2b9b396e3c938ade86a60b94259e567'

axios.defaults.baseURL = `${baseDomain}/api/`
axios.defaults.timeout = 1000
axios.defaults.headers = { 'Authorization': `Token ${token}` }

// login method
// if successfull, get the token, and update the instance's header


const urls = {
    'users': 'users/',
    'menus': 'menus/',
    'menu-item': 'menu-items/'
}

const api = {
    async get(item) {
        let url = urls[item]
        return (await axios.get(url)).data
    },
    async getSpecific(item, id) {
        let url = urls[item] + `${id}/` 
        return (await axios.get(url)).data
    },
    post(item, data) {
        let url = urls[item]
        return axios.post(url, data)
    },
    put(item, id, data) {
        let url = urls[item] + `${id}/`
        axios.put(url, data)
    },
    patch(item, id, data) {
        let url = urls[item] + `${id}/`
        axios.patch(url, data)
    },
}

export default api