import axios from 'axios'

class Client {
  constructor() {
    this.client = axios.create({
      baseURL: 'http://localhost:8000',
      withCredentials: false,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
    })
        // Add a response interceptor
    this.client.interceptors.response.use(function (response) {
      // Do something with response data
      return response;
    }, function (error) {
      if (error.response)
        console.error(error.response)
      return Promise.reject(error);
});
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
  async getProjectTasks({taskId}) {
    let res = await this.client.get(`/projects/tasks/${taskId}/`)
    return res
  }
  async deleteStatementsForSims({data}) {
    let res = await this.client.delete('/projects/simulation/delete_all_statements/', {data})
    return res
  }
  async checkStatementExists({params}) {
    let res = await this.client.get('/projects/statement/exists/', {params})
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
  async getWeatherStationRegions() {
    let res = await this.client.get('/products/weather-stations/regions/')
    return res
  }
  async getWeatherDataTypes(params) {
    let res = await this.client.get('/products/weather-data/get-types/', {params})
    return res
  }
  async getWeatherDataVariables(params) {
    let res = await this.client.get('/products/weather-data/get-variables/', {params})
    return res
  }
  async getWeatherDataPeriods(params) {
    let res = await this.client.get('/products/weather-data/get-periods/', {params})
    return res
  }
  async stationDryBulbSimulation(params) {
    let res = await this.client.post('/products/weather-data/dry-bulb-simulation/', params)
    return res
  }
  async getRejectionTemperatureImpact(params) {
    let res = await this.client.post('/products/heat-rejection/temperature-impact/', params)
    return res
  }
  async getRejectionTemperaturePayback(params) {
    let res = await this.client.post('/products/heat-rejection/temperature-payback/', params)
    return res
  }
}

const client = new Client()

export default client