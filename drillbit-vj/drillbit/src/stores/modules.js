import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

import client from '../services/client'

export const productPlugin = ({store}) => {
  store.object = ref(null)
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
  store.updateObjects = async () => {
    return client.bulkUpdateObjects({
      app: store.app, 
      model: store.dataModel, 
      params: {data: store.objects}
    }).then((result) => {
      store.objects = result.data
    })
  }
}

export const useRigStore = defineStore('rigStore', () => {
  const app = 'products'
  const dataModel = 'rigs'

  return { app, dataModel }
})

export const useCoolingStore = defineStore('coolingStore', () => {
  const app = 'products'
  const dataModel = 'cooling'

  return { app, dataModel }
})
export const useRejectionStore = defineStore('rejectionStore', () => {
  const app = 'products'
  const dataModel = 'rejection'

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
  const projects = ref([])

  return { projects }
})

export const useInputStore = defineStore('inputStore', () => {
  const blockScheduleStore = useBlockScheduleStore()
  const btcPriceStore = useBTCPriceStore()
  const feeStore = useFeeStore()
  const hashRateStore = useHashRateStore()
  

  const locked = ref({
    blockSchedule: false,
    btcPrice: false,
    fee: false,
    hashRate: false,
  })
  const lockable = computed(() => {
    return {
      blockSchedule: blockScheduleStore.hasObject,
      btcPrice: locked.value.blockSchedule && btcPriceStore.hasObject && btcPriceStore.object?.blocks === blockScheduleStore.object?.id,
      fee: locked.value.blockSchedule && feeStore.hasObject && feeStore.object?.blocks === blockScheduleStore.object?.id,
      hashRate: locked.value.blockSchedule && blockScheduleStore.hasObject && hashRateStore.object?.blocks === blockScheduleStore.object?.id,
  }})
  return {lockable, locked}
})