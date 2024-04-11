import { apiClient } from "@/api/clients"

export class Model {

  constructor(client, path) {
    this.client = client
    this.path = path
  }

  create(data) {
    return this.client.post(this.path, data)
  }

  getList(params) {
    return this.client.get(this.path, params)
  }

  get(id) {
    return this.client.get(this.path + id)
  }

  delete(id) {
    return this.client.delete(this.path + id + '/')
  }
}


export const blogPostModel = new Model(apiClient, '/blog/')
export const imageModel = new Model(apiClient, '/images/')
export const publicUserModel = new Model(apiClient, '/public-users/')
export const userModel = new Model(apiClient, '/users/')