import { ref, computed, watch } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useStorage } from '@vueuse/core'

import client from '../services/client'
import { useGlobalStateStore } from './globalState'

import { getTodayAsString, useFormHelpers, useFormatHelpers } from '../services/composables'
const {numberRules, numberIfNotNullRules, startDateRules, endDateRules} = useFormHelpers()

// Plugin containing common methods used amongst all stores
// Some methods can be overwritten by the store; these are captured in the if statements
// checking for the existence of the attribute (store.$state) or method in the store
export const productPlugin = ({store}) => {
  if (!Object.keys(store.$state).includes('object')) {
    store.object = ref(null)
  }
  if (!Object.keys(store.$state).includes('objects')) {
    store.objects = ref([])
  }
  store.hasObjects = computed(() => store.objects.length > 0)
  store.hasObject = computed(() => store.object != null)

  store.getObjects = async (params=null) => {
    return client.getObjects({app: store.app, model: store.dataModel, params})
      .then((result) => {
        store.objects = result.data
      })
  }
  store.getObject = async ({pk, params}) => {
    return client.getObjectsByPK({app: store.app, model: store.dataModel, pk, params})
      .then((result) => {
        store.object = result.data
      })
  }
  store.setObject = (object) => {
    store.object = object
  }
  store.setObjects = (objects) => {
    store.objects = objects
  }
  if (!Object.keys(store).includes('createObjects')) {
    store.createObjects = async ({params}) => {
      return client.createObjects({
        app: store.app, 
        model: store.dataModel,
        params
      }).then((result) => {
        // If return value is an array, store as objects, else store as object
        if (Array.isArray(result.data))
          {store.objects = result.data
          }
        else
          store.object = result.data
        })  
    } 
  }
  store.createObject = async ({params}) => {
    return client.createObject({
      app: store.app,
      model: store.dataModel,
      params
    }).then((result) => {
      store.object = result.data
    })
  }
  store.updateObject = async({pk, params}) => {
    return client.updateObject({
      app: store.app,
      model: store.dataModel,
      pk,
      params,
    }).then((result) => {
      store.object = result.data
    })
  }
  store.updateObjects = async () => {
    return client.bulkUpdateObjects({
      app: store.app, 
      model: store.dataModel, 
      params: {data: store.objects}
    }).then((result) => {
      store.objects = result.data
    })
  }
  store.updateOrCreateObject = async({pk, params}) => {
    if (pk)
      promise = store.updateObject({pk, params})
    else
      promise = store.createObject({params})

    promise.then((result) => {store.objects = result.data})
  }
  store.deleteObject = async (pk) => {
    return client.deleteObject({
      app: store.app, 
      model: store.dataModel, 
      pk
    })
  }
  store.findObjectById = (id) => {
    return store.objects.find((obj) => obj.id === id)
  }
  store.resetObject = () => {
    store.object = null
  }
}

/* PRODUCT STORES */
export const useRigStore = defineStore('rigStore', () => {
  const app = 'products'
  const dataModel = 'rig'

  return { app, dataModel }
})
export const useCoolingStore = defineStore('coolingStore', () => {
  const app = 'products'
  const dataModel = 'cooling'

  return { app, dataModel }
})
export const useRejectionStore = defineStore('rejectionStore', () => {
  const app = 'products'
  const dataModel = 'heat-rejection'

  return { app, dataModel }
})
export const useElectricalStore = defineStore('electricalStore', () => {
  const app = 'products'
  const dataModel = 'electrical'

  return { app, dataModel }
})
export const useCurveStore = defineStore('curveStore', () => {
  const app = 'products'
  const dataModel = 'heat-rejection-curve'

  return { app, dataModel }
})
export const useWeatherStationStore = defineStore('weatherStationStore', () => {
  const app = 'products'
  const dataModel = 'weather-stations'

  const regions = ref([])

  const getRegions = async () => {
    return client
      .getWeatherStationRegions()
      .then((result) => {
        regions.value = result.data
      })
  }

  return { app, dataModel, getRegions, regions }
})
export const useWeatherDataStore = defineStore('weatherDataStore', () => {
  const app = 'products'
  const dataModel = 'weather-data'

  const types = ref([])
  const variables = ref([])
  const periods = ref([])

  const getTypes = async (params) => {
    let res = await client.getWeatherDataTypes(params)
    types.value = res.data
  }
  const getPeriods = async (params) => {
    let res = await client.getWeatherDataPeriods(params)
    periods.value = res.data
  }
  const getVariables = async (params) => {
    let res = await client.getWeatherDataVariables(params)
    variables.value = res.data
  }

  return { app, dataModel, types, variables, periods, getTypes, getVariables, getPeriods }
})

/* ENVIRONMENT STORES */
function useForecastModelForm() {
  // Composable to manage creation of form for the various environment models
  const stateStore = useCurrentStateStore()
  const blockStore = useBlockScheduleStore()
  
  const initFormParams = {
    model: 'GBM',
    mean: .000025 * 100,
    volatility: .00701 * 100,
    initial: 0,
  }
  const globalState = useGlobalStateStore()
  const models = globalState.allowedTimeSeriesModels

  const initFormFields = (formParams) => {
    return [
      { name: 'model', label: 'Model', items: models, type: 'select' },
      { name: 'initial', label: 'Initial', prefix: '$', rules: numberRules.value },
      { 
        name: 'mean', 
        label: 'Mean', 
        suffix: '%',
        rules: numberIfNotNullRules.value,
        disabled: formParams.model === 'Constant'
      },
      { 
        name: 'volatility', 
        label: 'Volatility',
        suffix: '%',
        rules: numberIfNotNullRules.value,
        disabled: formParams.model === 'Constant' || formParams.model === 'CGR'
      },
    ]
  }
  const initCreateParams = (formParams) => {
    const params = {...formParams}
    params['mean'] = params.mean / 100
    params['volatility'] = params.volatility / 100
    params.blocks = blockStore.object?.id
    
    return params
  }
  return { initFormParams, initFormFields, initCreateParams, stateStore }
}
export const useCurrentStateStore = defineStore('currentStateStore', () => {
  const app = 'environment'
  const dataModel = 'current-state'

  return { app, dataModel }
})
export const useBlockScheduleStore = defineStore('blockScheduleStore', () => {
  
  const app = 'environment'
  const dataModel = 'block-schedule'

  const formParams = ref({start_date: getTodayAsString(), last_epoch: 5})
  const createParams = formParams

  const formFields = [
    { name: 'start_date', label: 'Start', rules: startDateRules },
    { name: 'last_epoch', label: 'End', hint: 'Date or Epoch', rules: endDateRules },
  ]

  return { app, dataModel, formParams, createParams, formFields }
  
})
export const useBTCPriceStore = defineStore('btcPriceStore', () => {
  const app = 'environment'
  const dataModel = 'bitcoin-price'
  const { initFormParams, initFormFields, initCreateParams, stateStore } = useForecastModelForm()

  const formParams = ref(initFormParams)
  const formFields = computed(() => initFormFields(formParams.value))
  watch(() => stateStore.objects, (objects) => {
    if (objects)
      formParams.value.initial = objects.Price
  })
  const createParams = computed(() => initCreateParams(formParams.value))

  return { app, dataModel, formParams, createParams, formFields }
})
export const useFeeStore = defineStore('feeStore', () => {
  const app = 'environment'
  const dataModel = 'transaction-fees'

  const { initFormParams, initFormFields, initCreateParams } = useForecastModelForm()
  const formParams = ref(initFormParams)
  formParams.value.initial = 0.078

  const formFields = computed(() => {
    let formFields = initFormFields(formParams.value)
    formFields[1].prefix = '\u20BF'
    return formFields
  })
  const createParams = computed(() => initCreateParams(formParams.value))

  return { app, dataModel, formParams, createParams, formFields }
})
export const useHashRateStore = defineStore('hashRateStore', () => {
  const app = 'environment'
  const dataModel = 'hash-rate'
  const { initFormParams, initFormFields, initCreateParams, stateStore } = useForecastModelForm()

  const formParams = ref(initFormParams)
  watch(() => stateStore.objects, (objects) => {
    if (objects) 
      formParams.value.initial = (stateStore.objects['Network Hash Rate'] / 1e18).toFixed(2)
  })
  const formFields = computed(() => {
    let formFields = initFormFields(formParams.value)
    formFields[1].prefix = ''
    formFields[1].suffix = ' EH/s'
    return formFields
  })  
  const createParams = computed(() => initCreateParams(formParams.value))

  return { app, dataModel, formParams, createParams, formFields }
})
export const useEnvironmentStore = defineStore('environmentStore', () => {
  const app = 'environment'
  const dataModel = 'environment'
  const blockScheduleStore = useBlockScheduleStore()
  const btcPriceStore = useBTCPriceStore()
  const feeStore = useFeeStore()
  const hashRateStore = useHashRateStore()

  let stores = {
    block_schedule: blockScheduleStore,
    bitcoin_price: btcPriceStore,
    transaction_fees: feeStore,
    hash_rate: hashRateStore,
  }
  const components = computed(() => {
    return {
      block_schedule: blockScheduleStore.object?.id,
      bitcoin_price: btcPriceStore.object?.id,
      transaction_fees: feeStore.object?.id,
      hash_rate: hashRateStore.object?.id,
    }
  })

  const object = ref(null)
  const clear = () => {
    object.value = null
    Object.values(stores).forEach((store) => {
      store.object = null
    })
  }
  const load = async (params) => {
    let promises = []
    let pk = params.id
    let result = await client.getObjectsByPK({app, model: dataModel, pk})
    object.value = result.data
    Object.entries(stores).forEach(([key, store]) => {
      let promise = client.getObjectsByPK({
        app: store.app, 
        model: store.dataModel, 
        pk: object.value[key]
      }).then(result => {
        store.object = result.data
        Object.keys(store.formParams).forEach((key) => {
          if (['mean', 'volatility'].includes(key)) // must adjust incoming values to fit form
            store.formParams[key] = store.object[key] * 100
          else
            store.formParams[key] = store.object[key]      
        })
      })
      promises.push(promise)
    })
    return Promise.all(promises)
  }
  const save = () => {
    let pk = object.value?.id ?? null
    let params = {name: object.value.name, ...components.value }
    return client
      .updateOrCreateObject({app, model: dataModel, pk, params})
      .then((result) => {
        object.value = result.data
      })
  }
  const locked = ref({
    blockSchedule: false,
    btcPrice: false,
    fee: false,
    hashRate: false,
  })
  const allLocked = computed(() => {
    return locked.value.blockSchedule 
      && locked.value.btcPrice
      && locked.value.fee
      && locked.value.hashRate
  })
  const lockable = computed(() => {
    return {
      blockSchedule: blockScheduleStore.hasObject,
      btcPrice: locked.value.blockSchedule && btcPriceStore.hasObject && btcPriceStore.object?.blocks === blockScheduleStore.object?.id,
      fee: locked.value.blockSchedule && feeStore.hasObject && feeStore.object?.blocks === blockScheduleStore.object?.id,
      hashRate: locked.value.blockSchedule && blockScheduleStore.hasObject && hashRateStore.object?.blocks === blockScheduleStore.object?.id,
  }})
  const allLockable = computed(() => {
    return blockScheduleStore.hasObject 
      && btcPriceStore.hasObject && btcPriceStore.object?.blocks === blockScheduleStore.object?.id
      && feeStore.hasObject && feeStore.object?.blocks === blockScheduleStore.object?.id
      && blockScheduleStore.hasObject && hashRateStore.object?.blocks === blockScheduleStore.object?.id
  })
  return {
    app, dataModel,
    object, components, 
    save, load, clear,
    lockable, locked, allLocked, allLockable
  }
},{
  persist: {
    storage: sessionStorage,
  },
})

/* Project Module */
export const useProjectStore = defineStore('projectStore', () => {
  const app = 'projects'
  const dataModel = 'project'

  const projects = ref([])
  const projectIds = computed(() => {
    return projects.value.map((obj) => obj.id)
  })
 
  const create = async (params) => {
    return client.createObjects({
      app: app, 
      model: dataModel,
      params
    }).then((result) => {
      projects.value.push(result.data)
    })
  }
  const update = async (params) => {
    let pk = params.id
    return client.updateObject({
      app: app, 
      model: dataModel,
      params,
      pk
    }).then((result) => {
      let index = projects.value.findIndex((obj) => obj.id === result.data.id)
      projects.value[index] = result.data
    })
  }
  const del = async (pk) => {
    return client.deleteObject({app, model: dataModel, pk}).then((result) => {
      projects.value = projects.value.filter((obj) => obj.id !== pk)
    })
  }
  const scale = async (pk) => {
    return client.scaleProject({app, model: dataModel, pk}).then((result) => {
      let index = projects.value.findIndex((obj) => obj.id === result.data.id)
      projects.value[index] = result.data
    })
  }
  const costs = async (pk) => {
    let result = await client.getProjectCosts({app, model: dataModel, pk})
    return result.data
  }
  return { app, dataModel, projects, projectIds, create, update, del, scale, costs }
})
export const useProjectsStore = defineStore('projectsStore', () => {
  const app = 'projects'
  const dataModel = 'projects'

  const projectStore = useProjectStore()
  const object = ref(null)
  const load = async (params) => {
    let pk = params.id
    return client
      .getObjectsByPK({app, model: dataModel, pk})
      .then((result) => {
        object.value = result.data
        projectStore.$patch((state) => {
          state.projects = result.data.projects
        })
    })
  }
  const save = async () => {
    let pk = object.value?.id ?? null
    let params = {name: object.value.name, project_ids: projectStore.projectIds}
    return client
      .updateOrCreateObject({app, model: dataModel, pk, params})
      .then((result) => {
        object.value = result.data
      })
  }
  
  return { app, dataModel, object, load, save }
  },{
    persist: {
      storage: sessionStorage,
  },
})
export const useSimulationStore = defineStore('simulationStore', () => {
  const app = 'projects'
  const dataModel = 'simulation'

  const envStore = useEnvironmentStore()
  const projectsStore = useProjectsStore()

  const simsByAttrs = computed(() => {
    let sims = []
    projectsStore.object.projects.forEach((project) => {
      sims.push({
        environment: envStore.object.id,
        project: project.id,
      })
    })
    return sims
  })
  const deleteStatements = async ({simsByIds}) => {
    return client.deleteStatementsForSims({data: simsByIds})
  }

  return { app, dataModel, simsByAttrs, deleteStatements }
})
export const useStatementStore = defineStore('statementStore', () => {
  const envStore = useEnvironmentStore()
  const projectsStore = useProjectsStore()
  const simStore = useSimulationStore()
  const app = 'projects'
  const dataModel = 'statement'

  const allowedFreqs = ['H', 'D', 'M', 'Q', 'A']

  const summary = ref(null)
  const byAccount = ref(null)
    
  const taskStatuses = ref({})
  const hasTasks = computed(() => Object.keys(taskStatuses.value).length > 0)
  const nTasksToComplete = computed(() => {
    return simStore.objects.length * allowedFreqs.length
  })
  const nTasksComplete = computed(() => {
    let nComplete = 0

    for (let sim of Object.keys(taskStatuses.value)) {
      for (let frequency of allowedFreqs) {
        if (taskStatuses.value[sim][frequency]['status'] === 'SUCCESS') {
          nComplete += 1
        }
      }
    }
    return nComplete
  })
  const allTasksComplete = computed(() => nTasksComplete.value === nTasksToComplete.value)
  
  const projectTasksComplete = computed(() => {
    let projectStatuses = {}
    if (hasTasks.value) {
      for (let [sim, statuses] of Object.entries(taskStatuses.value)) {
        let simObj = simStore.objects.find((obj) => obj.id === Number(sim))
        projectStatuses[simObj.project] = allowedFreqs.every((freq) => statuses[freq].status === 'SUCCESS')
      }
    }
    return projectStatuses
  })
  const initStatus = (tasksBySim) => {
    for (let [sim, tasks] of Object.entries(tasksBySim)) {
      taskStatuses.value[sim] = {}
      for (let [frequency, taskId] of Object.entries(tasks)) {
        taskStatuses.value[sim][frequency] = {}
        taskStatuses.value[sim][frequency]['task_id'] = taskId
        taskStatuses.value[sim][frequency]['status'] = null
      }
    }
  }
  const fetchStatus = () => {
    Object.entries(taskStatuses.value).forEach(([sim, tasks]) => {
      Object.entries(tasks).forEach(([frequency, task]) => {
        checkTaskComplete(task['task_id'], 2000, (result) => {
          taskStatuses.value[sim][frequency]['status'] = result.state
        })
      })
    })
  }
  const checkTaskComplete = (taskId, interval, callback) => {
    var counter = 0
    let intervalId = setInterval(() => {
      client.getProjectTasks({taskId}).then((result) => {
        try {
          if (result.data.state === 'SUCCESS') {
            clearInterval(intervalId)
            callback(result.data)
          } else {
            counter++
            if (counter > 100) {
              clearInterval(intervalId)
              console.log('task did not complete')
              throw new Error('Max retries exceeded')
            }
          }
        } catch (err) {
          counter++
          clearInterval(intervalId)
          if (counter > 2) {
            console.log('an error was thrown and caught')
            throw new Error('Max retries exceeded')
          }
        }
      }).catch((err) => {
        console.error(err)
        clearInterval(intervalId) // this will stop the interval
      })
    }, interval)
  }
  const createObjects = async ({params, overwrite}) => {
    /* 
    Logic for creating statements:
    1. Check if statements exist for the given environment and projects
    2. If they do, get the summary and byAccount
    3. If they don't, create the statements

    If overwrite is true, delete the existing statements first; thus response to 1. above will always be false

    The main BLOCK level statement and the summary statement are created synchronously. So, the summary table is
    fetched immediately after the main monthly statement is created. 
    
    The other periods ['H', 'D', 'M', 'Q', 'A'] are all created asynchronously and so a task_id is 
    returned for each. Completion is monitored by status checks on the task_id. Before the task is 
    complete, the byAccount data for the period is not available.
    */

    var objParams = {
      environment: envStore.object.id,
      projects: projectsStore.object.projects.map((project) => project.id),
      frequency: params.frequency,
    }
    if (overwrite) {
      await simStore.deleteStatements({
        simsByIds: simStore.objects.map((sim) => sim.id)
      })
    }
    const res = await client.checkStatementExists({params: objParams})
    if (res.data) {
      getSummary({params: objParams})
      getByAccount({params: objParams})    
    } else { 
      return client.createObjects({
        app, 
        model: dataModel,
        params
      }).then((result) => {
        getSummary({params: objParams})
        initStatus(result.data)
        fetchStatus()
      })
    } 
  }
  const getSummary = async ({params}) => {
    return client.getStatSummary({params}).then((result) => { 
        summary.value = result.data
    })
  }
  const getByAccount = async ({params}) => {
    return client.getStatByAccount({params}).then((result) => { 
      byAccount.value = result.data
    })
  }  
  return { 
    app, dataModel, allowedFreqs, 
    createObjects, summary, getSummary, 
    byAccount, getByAccount,
    taskStatuses, hasTasks, nTasksComplete, nTasksToComplete, allTasksComplete,
    projectTasksComplete,
  }
  }, {
    persist: {
      storage: sessionStorage,
    },
  }
)
