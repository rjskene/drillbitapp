<script setup>
import { ref, toRefs, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'

import { useAsyncState } from '@vueuse/core'

import Skeleton from 'primevue/skeleton'

import StatefulBtn from '../../reuseable/StatefulBtn.vue'
import CrudBar from '@/components/reuseable/CrudBar.vue'
import MainWindow from '../MainWindow.vue'
import EnvironmentSummary from './EnvironmentSummary.vue'
import FactorForm from './FactorForm.vue'
import Chart from '@/components/reuseable/Chart.vue'
import PlaceholderChart from '../../reuseable/PlaceholderChart.vue'

import { 
  useBlockScheduleStore, useBTCPriceStore, useFeeStore, useHashRateStore,
  useEnvironmentStore
} from '@/stores/modules'
import { every_nth, useFormHelpers } from '@/services/composables'

const store = useEnvironmentStore()

const formHelpers = useFormHelpers()

const summaryActive = ref(false)
const activeIndex = ref(0)
const elements = [
  {text: 'Block Schedule',  store: useBlockScheduleStore(), yLabel: 'reward'},
  {text: 'BTC Price', store: useBTCPriceStore(), yLabel: 'forecast'},
  {text: 'Transaction Fees', store: useFeeStore(), yLabel: 'forecast'},
  {
    text: 'Network Hash Rate', 
    store: useHashRateStore(), 
    yLabel: 'forecast',
    xTickPrefix: '',
    xTickSuffix: 'M TH/s'
  }
]
const activeElement = computed(() => {
  return elements[activeIndex.value]
})
const activeStore = computed(() => {
  return activeElement.value.store
})
const activeName = computed(() => {
  return activeStore.value.$id.replace('Store', '')
})
const elementName = (element) => {
  return element.store.$id.replace('Store', '')
}

const createState = ref({})
const load = (params) => {
  if (typeof params === 'string' || params instanceof String) {
    store.$patch((state) => {
      state.object.name = params
    })
  } else if (!params) {
    // pass
  } else {
    createState.value = useAsyncState(
      store.load(params),
      {},
      {
        onError: (error) => {
          console.error(error.response)
        }
      }
    )}
}
const create = (element) => {
  let state = useAsyncState(
    element.store.createObjects({params: element.store.createParams}),
    {},
    {
      onError: (error) => {
        console.error(error.response)
      }
    }
  )
  createState.value = state
  return state
}

const form = ref(null)
const locked = (name) => {
  return store.locked[name]
}
const lockable = (name) => {
  return store.lockable[name]
}
const lock = (name) => {
  if (lockable(name) & form.value.valid) {
    store.$patch(() => {
      store.locked[name] = true
    })
  }
}
const lockAll = () => {
  elements.forEach((element) => {
    lock(elementName(element))
  })
}
const unlockAll = () => {
  elements.forEach((element) => {
    unlock(elementName(element))
  })
}
const unlock = (name) => {
  store.$patch(() => {
    store.locked[name] = false
  })
}
const readyOrNot = (name) => {
  return {
    icon: store.locked[name] ? 'mdi-check' : 'mdi-close',
    color: store.locked[name] ? 'secondary' : 'error'
  }
}
</script>
  
<template>
  <MainWindow>
    <template #nav-panel>
      <v-combobox
        @update:modelValue="(params) => load(params)"
        @click:clear="store.clear"
        :items="formHelpers.reverse(store.objects)"
        label="Environment"
        item-title="name"
        density="compact"
        outlined
        clearable
        class="mt-0 pl-3 pr-1"
      >
      <template #append>
        <StatefulBtn
          @click="store.save"
          variant="flat"
          icon="mdi-content-save"
          size="x-small"
          :disabled="!store.allLocked"
        />
        <v-btn
          v-if="!store.allLocked"
          @click="lockAll"
          icon="mdi-lock-open-variant"
          size="x-small"
          variant="flat"
          :disabled="!store.allLockable"
          class="mr-0 pr-0"
        />
        <v-btn
          v-else
          id="div"
          @click="unlockAll"
          icon="mdi-lock"
          variant="flat"
          size="x-small"
        />
        </template>
      </v-combobox>
      <v-list-item
        @click="activeIndex = -1"
        class="pl-3"
      >
        Summary
      </v-list-item>
      <v-list-item
        v-for="(element, i) in elements"
        @click="activeIndex = i"
        :key="element.text + '-element'"
        :value="element.value"
        class="pl-3 pr-1"
      >
        {{ element.text }}
        <template #append>
          <v-icon
            v-bind="readyOrNot(elementName(element))"
            class="ml-1 mr-1 pr-0"
            size="x-small"
          />
          <StatefulBtn
            @click="create(element)"
            variant="flat"
            icon="mdi-content-save"
            size="x-small"
            :disabled="locked(elementName(element))"
          />
          <v-btn
            v-if="locked(elementName(element))"
            @click="unlock(elementName(element))"
            icon="mdi-lock"
            variant="flat"
            size="x-small"
            class="mr-0 pr-0"
          ></v-btn>
          <v-btn
            v-else
            @click="lock(elementName(element))"
            icon="mdi-lock-open-variant"
            variant="flat"
            size="x-small"
            :disabled="!lockable(elementName(element))"
            class="mr-0 pr-0"
            ></v-btn>
        </template>
      </v-list-item>
    </template>
    <template #main-panel>
        <EnvironmentSummary
          v-if="activeIndex === -1"
          :elements="elements"
        />
        <FactorForm
          v-else
          ref="form"
          :create-state="createState"
          :active-element="activeElement"
        />
    </template>
  </MainWindow>
</template>
  
<style scoped>
::v-deep(.p-skeleton) {
  background-color: rgb(var(--v-theme-surface));
}
</style>