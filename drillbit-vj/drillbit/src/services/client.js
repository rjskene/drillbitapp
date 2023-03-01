import axios from 'axios'

class Client {
  constructor() {
    this.client = axios.create({
      baseURL: 'http://localhost:8000',
      withCredentials: false,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    })
  }
  async getObjects({app, model, params}) {
    let res = await this.client.get(`/${app}/${model}/`, {params})
    return res
  }
  async getObjectsByPK({app, model, pk, params}) {
    let res = await this.client.get(`/${app}/${model}/${pk}/`, {params})
    return res
  }
  async createObjects({app, model, params}) {
    let res = await this.client.post(`/${app}/${model}/`, params)
    return res
  }
  async updateObject({app, model, pk, params}) {
    let res = await this.client.put(`/${app}/${model}/${pk}/`, params)
    return res
  }
  async deleteObject({app, model, pk}) {
    let res = await this.client.delete(`/${app}/${model}/${pk}/`)
    return res
  }
  async updateOrCreateObject({app, model, pk, params}) {
    let res
    if (pk)
      res = await this.updateObject({app, model, pk, params})
    else
      res = await this.createObjects({app, model, params})
    return res
  }
  async bulkUpdateObjects({app, model, params}) {
    let res = await this.client.put(`/${app}/${model}/bulk-update/`, params)
    return res
  }
  async scaleProject({app, model, pk}) {
    let res = await this.client.put(`/${app}/${model}/${pk}/scale/`)
    return res
  }
  async getProjectCosts({app, model, pk}) {
    let res = await this.client.get(`/${app}/${model}/${pk}/costs/`)
    return res
  }
  async getProjectTasks({task_id}) {
    let res = await this.client.get(`/projects/tasks/${task_id}`)
    return res
  }
  async getStatSummary({params}) {
    let res = this.client.get('/projects/summary/', {params})
    return res
  }
  async getStatByAccount({params}) {
    let res = this.client.get('/projects/statement/projects_by_account/', {params})
    return res
  }
}

const client = new Client()

export default client