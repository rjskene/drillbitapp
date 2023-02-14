import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

import client from '../services/client'

export const productPlugin = ({store}) => {
  if (!Object.prototype.hasOwnProperty(store.$state, 'object')) {
    store.object = ref(null)
  }
  store.objects = ref([])
  store.hasObjects = computed(() => store.objects.length > 0)
  store.hasObject = computed(() => store.object != null)

  store.getObjects = async () => {
    return client.getObjects({app: store.app, model: store.dataModel})
      .then((result) => {
        store.objects = result.data
      })
  }
  store.getObject = async ({pk}) => {
    return client.getObjectsByPK({app: store.app, model: store.dataModel, pk})
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

export const useBlockScheduleStore = defineStore('blockScheduleStore', () => {
  const app = 'environment'
  const dataModel = 'block-schedule'
  
  return { app, dataModel }
  
})
export const useBTCPriceStore = defineStore('btcPriceStore', () => {
  const app = 'environment'
  const dataModel = 'bitcoin-price'
  
  return { app, dataModel }

})
export const useFeeStore = defineStore('feeStore', () => {
  const app = 'environment'
  const dataModel = 'transaction-fees'
  
  return { app, dataModel }
})
export const useHashRateStore = defineStore('hashRateStore', () => {
  const app = 'environment'
  const dataModel = 'hash-rate'
  
  return { app, dataModel }
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
    let result = await client.getObjectsByPK({app, model: dataModel, pk})
    object.value = result.data
    projectStore.$patch((state) => {
      state.projects = result.data.projects
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

  const environment = ref({name: null})

  const components = computed(() => {
    return {
      block_schedule: blockScheduleStore.object?.id,
      bitcoin_price: btcPriceStore.object?.id,
      transaction_fees: feeStore.object?.id,
      hash_rate: hashRateStore.object?.id,
    }
  })

  const save = () => {
    let pk = environment.value?.id ?? null
    let params = {name: environment.value.name, ...components.value }
    return client
      .updateOrCreateObject({app, model: dataModel, pk, params})
      .then((result) => {
        environment.value = result.data
      })
  }
  
  const load = async (params) => {
    let pk = params.id
    let result = await client.getObjectsByPK({app, model: dataModel, pk})
    environment.value = result.data
    Object.entries(stores).forEach(([key, store]) => {
      client.getObjectsByPK({
        app: store.app, 
        model: store.dataModel, 
        pk: environment.value[key]
      }).then(result => {
        store.object = result.data
      })
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
  return {
    app, dataModel,
    environment, components, 
    save, load,
    lockable, locked, allLocked 
  }
})