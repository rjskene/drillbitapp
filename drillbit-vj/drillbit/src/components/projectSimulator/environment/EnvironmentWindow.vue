<script setup>
import { ref, toRefs, watch, computed } from 'vue'

import { useAsyncState } from '@vueuse/core'

import StatefulBtn from '../../reuseable/StatefulBtn.vue'
import MainWindow from '../MainWindow.vue'
import EnvironmentSummary from './EnvironmentSummary.vue'
import FactorForm from './FactorForm.vue'

import { 
  useBlockScheduleStore, useBTCPriceStore, useFeeStore, useHashRateStore,
  useEnvironmentStore
} from '@/stores/modules'
import { useFormHelpers, useFormatHelpers } from '@/services/composables'

const formHelpers = useFormHelpers()
const store = useEnvironmentStore()

const activeIndex = ref(-1)
const elements = [
  {
    text: 'Block Schedule',  
    store: useBlockScheduleStore(), 
    dataKey: 'reward',
    chartOptions: {
      yTickFormat: 'BTC',
    }
  },
  {
    text: 'BTC Price', 
    store: useBTCPriceStore(), 
    dataKey: 'forecast',
    chartOptions: {
      yTickFormat: 'currency',
      yTickFormatOptions: {maximumFractionDigits: 0}
    }
  },
  {
    text: 'Transaction Fees', 
    store: useFeeStore(), 
    dataKey: 'forecast',
    chartOptions: {
      yTickFormat: 'BTC',
      yTickFormatOptions: {toFixed: 2}
    }
  },
  {
    text: 'Network Hash Rate',
    store: useHashRateStore(),
    dataKey: 'forecast',
    chartOptions: {
      yTickFormat: 'hashRate',
    }
  }
]
const activeElement = computed(() => {
  return elements[activeIndex.value]
})
const elementName = (element) => {
  return element.store.$id.replace('Store', '')
}

const loadState = ref({})
const load = (params) => {
  console.log('load', params)
  if ((typeof params === 'string' || params instanceof String)) {
    store.$patch((state) => {
      state.object = {name: params}
    })
  } else if (params) {
    loadState.value = useAsyncState(
      store.load(params),
      {},
      {
        onError: (error) => {
          console.error(error.response)
        }
      }
    )
    loadState.value.execute().then(() => {
      for (let element of elements) {
        store.$patch(() => {
          store.locked[elementName(element)] = true
        })
      }
    })
  }
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
  loadState.value = state
  return state
}

const form = ref(null)
const locked = (name) => {
  return store.locked[name]
}
const lockable = (name) => {
  return store.lockable[name]
}
const lock = (name, noFormValidation = false) => {
  if (lockable(name) & (noFormValidation || form.value.valid )) {
    store.$patch(() => {
      store.locked[name] = true
    })
  }
}
const lockAll = () => {
  elements.forEach((element) => {
    lock(elementName(element), true)
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
      <v-list>
        <v-list-item
          @click="activeIndex = -1"
          key="summary-element"
          value="-1"
          class="pl-3"
        >
          Summary
        </v-list-item>
        <v-list-item
          v-for="(element, i) in elements"
          @click="activeIndex = i"
          :key="element.text + '-element'"
          :value="i"
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
      </v-list>
    </template>
    <template #main-panel>
      <EnvironmentSummary
        v-if="activeIndex === -1"
        :elements="elements"
        :environment="store.object"
        :loading="loadState.isLoading"
      />
      <FactorForm
        v-else
        ref="form"
        :create-state="loadState"
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