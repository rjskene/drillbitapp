import { ref, computed, watch } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useStorage } from '@vueuse/core'


import client from '../services/client'
import { useGlobalStateStore } from './globalState'

export const productPlugin = ({store}) => {
  if (!Object.keys(store.$state).includes('object')) {
    store.object = ref(null)
  }
  if (!Object.keys(store.$state).includes('object')) {
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
          store.objects = result.data
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
  store.udpateObject = async({pk, params}) => {
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
  store.findObjectById = (id) => {
    return store.objects.find((obj) => obj.id === id)
  }
  store.resetObject = () => {
    store.object = null
  }
}

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

import { getTodayAsString, useFormHelpers, useEnviroForm } from '../services/composables'
const {nameRules, numberRules, numberIfNotNullRules, startDateRules, endDateRules} = useFormHelpers()

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
function useForecastModelForm() {
  const blockStore = useBlockScheduleStore()
  const stateStore = useCurrentStateStore()
  const {objects: stateObject } = storeToRefs(stateStore)
  
  const formParams = ref({
    model: 'GBM',
    initial: 20000,
    mean: .000025,
    volatility: .00701,

  })
  watch(stateObject, (object) => {
    if (object)
      formParams.value.initial = object.Price
  })

  const createParams = computed(() => {
    const params = {...formParams.value}
    params.blocks = blockStore.object?.id
    return params
  })
  const globalState = useGlobalStateStore()
  const models = globalState.allowedTimeSeriesModels

  const formFields = [
    { name: 'model', label: 'Model', items: models, type: 'select' },
    { name: 'initial', label: 'Initial', prefix: '$', rules: numberRules },
    { 
      name: 'mean', 
      label: 'Mean', 
      rules: numberIfNotNullRules,
      disabled: computed(() => formParams.value.model === 'Constant') 
    },
    { 
      name: 'volatility', 
      label: 'Volatility',
      rules: numberIfNotNullRules,
      disabled: computed(() => formParams.value.model === 'Constant' || formParams.value.model === 'CGR') 
    },
  ]
  return { formParams, createParams, formFields }
}

export const useBTCPriceStore = defineStore('btcPriceStore', () => {
  const app = 'environment'
  const dataModel = 'bitcoin-price'
  const { formParams, createParams, formFields } = useForecastModelForm()

  return { app, dataModel, formParams, createParams, formFields }
})
export const useFeeStore = defineStore('feeStore', () => {
  const app = 'environment'
  const dataModel = 'transaction-fees'
  const { formParams, createParams, formFields } = useForecastModelForm()
  formFields[1].prefix = '\u20BF'

  return { app, dataModel, formParams, createParams, formFields }
})
export const useHashRateStore = defineStore('hashRateStore', () => {
  const app = 'environment'
  const dataModel = 'hash-rate'
  const { formParams, createParams, formFields } = useForecastModelForm()
  formFields[1].prefix = ''
  formFields[1].suffix = 'M TH/s'

  return { app, dataModel, formParams, createParams, formFields }
})
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

  return { app, dataModel }
})

export const useStatementStore = defineStore('statementStore', () => {
  const envStore = useEnvironmentStore()
  const projectsStore = useProjectsStore()
  const app = 'projects'
  const dataModel = 'statement'

  const summary = ref(null)
  const byAccount = ref(null)

  const object = ref(null)
  const objects = ref([])

  const taskStatuses = ref({})
  const tasksComplete = computed(() => {
    return Object.values(taskStatuses.value).length > 0 
      && Object.values(taskStatuses.value).every((status) => status === 'SUCCESS')
  })        

  const checkTaskComplete = (task_id, interval, callback) => {
    var counter = 0
    let intervalId = setInterval(() => {
      client.getProjectTasks({task_id}).then((result) => {
        try {
          if (result.data.state === 'SUCCESS') {
            clearInterval(intervalId)
            callback(result.data)
          } else {
            counter++
            if (counter > 10) {
              clearInterval(intervalId)
              throw new Error('Max retries exceeded')
            }
          }
        } catch (err) {
          console.error(err)
          clearInterval(intervalId)
        }
      })
    }, interval)
  } 
  const fetchStatus = () => {
    Object.keys(taskStatuses.value).forEach((task_id) => {
      checkTaskComplete(task_id, 1000, (result) => {
        taskStatuses.value[task_id] = result.state
      })
    })
  }
  const createObjects = async ({params}) => {
    var objParams = {
      environment: envStore.object.id,
      projects: projectsStore.object.projects.map((project) => project.id)
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
        let task_ids = result.data.map((obj) => obj['M'])
        taskStatuses.value = {} // need to reset 
        task_ids.forEach((task_id) => {taskStatuses.value[task_id] = null})
        
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
    app, dataModel, object, objects, createObjects, summary, getSummary, 
    byAccount, getByAccount,
    taskStatuses, tasksComplete
  }
  }, {
    persist: {
      storage: sessionStorage,
    },
  }
)

export const useCurrentStateStore = defineStore('currentStateStore', () => {
  const app = 'environment'
  const dataModel = 'current-state'

  return { app, dataModel }
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

  const object = ref({name: null})
  const clear = () => {
    object.value = {name: null}
  }
  const load = async (params) => {
    let pk = params.id
    let result = await client.getObjectsByPK({app, model: dataModel, pk})
    object.value = result.data
    Object.entries(stores).forEach(([key, store]) => {
      client.getObjectsByPK({
        app: store.app, 
        model: store.dataModel, 
        pk: object.value[key]
      }).then(result => {
        store.object = result.data
        Object.keys(store.formParams).forEach((key) => {
          store.formParams[key] = store.object[key]
        })
      })
    })
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