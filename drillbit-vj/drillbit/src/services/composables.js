import { ref, computed, watch, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { useAsyncState, useRefHistory } from '@vueuse/core'

import { useGlobalStateStore } from '../stores/globalState'

export function hexToRGB (hex, opacity=null, asString=False) {
  let rgb = hex.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i
    ,(m, r, g, b) => '#' + r + r + g + g + b + b)
    .substring(1).match(/.{2}/g)
    .map(x => parseInt(x, 16))
  if (opacity)
    rgb.push(opacity)
  if (asString) {
    let prefix = opacity ? 'rgba' : 'rgb'
    return `${prefix}(${rgb.join(',')})`
  }
  else
    return rgb
}
export const every_nth = (arr, nth) => arr.filter((e, i) => i % nth === nth - 1)

export function useFormatHelpers() {
  const btcStr = '\u20BF'
  const date = (dateStr) => {
    let dateObj = new Date(dateStr)
    return dateObj.toLocaleString()
  }

  const percentage = (value) => {
    return (value*100).toFixed(2) + '%'
  }
  const number = (value, {toFixed = 0} = {}) => {
    if (isValidNumber(value))
      return value.toFixed(toFixed).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    else
      return value
  }
  const temperature = (value) => {
    if (value)
      return value.toFixed(0) + '°F'
    return value
  }
  const BTC = (value, {toFixed = 0} = {}) => {
    return '\u20BF ' + value.toFixed(toFixed).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
  const T = (value) => {
    return (value / 1e12).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + 'T'
  }
  const currency = (value, {style='', maximumFractionDigits = 2} = {}) => {
    let NF = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits })
    if (style === 'M')
      value = Math.round(value/10000)/100
    if (style === 'K')
      value = Math.round(value/10)/100
  
    return NF.format(value) + style
  }
  const scaler = (value, units, toFixed=0) => {
    let i = 0
    while (value >= 1000) {
      value = value/1000
      i++
    }
    if (value)
      return value.toFixed(toFixed) + ' ' + units[i]
    else
      return null
  }
  const inverseScaler = (value, units, toFixed=0) => {
    if (value === 0) return value
    else if (value < 0) throw new Error('Value must be positive')
    
    let i = 0
    while (value < 1) {
      value = value*1000
      i++
    }
    if (value)
      return value.toFixed(toFixed) + ' ' + units[i]
    else
      return null
  }  
  const hashes = (value, {toFixed = 0} = {}) => {
    let units = ['H', 'KH', 'MH', 'GH', 'TH', 'PH', 'EH', 'ZH', 'YH', 'RH']
    return scaler(value, units, toFixed)
  }
  const hashRate = (value, {toFixed = 0} = {}) => {
    let units = ['H/s', 'KH/s', 'MH/s', 'GH/s', 'TH/s', 'PH/s', 'EH/s', 'ZH/s', 'YH/s', 'RH/s']
    return scaler(value, units, toFixed)
  }
  const power = (value, {toFixed = 0} = {}) => {
    let units = ['W', 'kW', 'MW', 'GW', 'TW', 'PW', 'EW', 'ZW', 'YW', 'RW']
    return scaler(value, units, toFixed)
  }
  const energy = (value, {toFixed = 0} = {}) => {
    let units = ['Wh', 'kWh', 'MWh', 'GWh', 'TWh', 'PWh', 'EWh', 'ZWh', 'YWh', 'RWh']
    return scaler(value, units, toFixed)
  }
  const efficiency = (value, {toFixed = 0} = {}) => {
    let units = ['J/H', 'J/KH', 'J/MH', 'J/GH', 'J/TH', 'J/PH', 'J/EH', 'J/ZH', 'J/YH', 'J/RH']
    return inverseScaler(value, units, toFixed)
  }
  const hashPrice = (value, {toFixed = 0} = {}) => {
    let units = ['$/H', '$/KH', '$/MH', '$/GH', '$/TH', '$/PH', '$/EH', '$/ZH', '$/YH', '$/RH']
    return inverseScaler(value, units, toFixed)
  }
  const energyPrice = (value, {toFixed = 0} = {}) => {
    let units = ['$/Wh', '$/KWh', '$/MWh', '$/GWh', '$/TWh', '$/PWh', '$/EWh', '$/ZWh', '$/YWh', '$/RWh']
    return inverseScaler(value, units, toFixed)
  }
  return { 
    date, btcStr, percentage, number, temperature, BTC, currency, T, 
    hashes, hashRate, power, energy, efficiency, hashPrice, energyPrice
  }
}

const format = useFormatHelpers()

export const dateAsString = (date) => {
  var dd = String(date.getDate()).padStart(2, '0');
  var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = date.getFullYear();
  
  date = yyyy + '-' + mm + '-' + dd;
  return date  
}
export const getTodayAsString = () => {
  var today = new Date();
  return dateAsString(today)
}
export const validateDateFormat = (string) => {
  // string should be in format yyyy-mm-dd
  const regex = new RegExp('^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
  return regex.test(string)
}
const isValidNumber = (v) => {
  let num = Number(v)
  return !Number.isNaN(num)
}
const dateOrWholeNumber = (v) => {
  if (validateDateFormat(v)) {
    return true
  } else {
    try {
      let num = Number(v)
      if (Number.isInteger(num) & num > 0) {
        return true
      }
    } catch (e) {
      return false
    }
  }
  return false
}
export function useFormHelpers() {
  const nameRules = computed(() => {
    let rules = [
      v => !!v || 'Name is required',
    ]
    return rules
  })
  const startDateRules = computed(() => {
    let rules = [
      v => !!v || 'Start date is required',
      v => validateDateFormat(v) || 'Invalid date format'
    ]
    return rules
  })
  const endDateRules = computed(() => {
    let rules = [
      v => !!v || 'End date is required',
      v => dateOrWholeNumber(v) || 'Must be date or integer'
    ]
    return rules
  })
  const numberRules = computed(() => {
    // array with two rules, second rule checks if value is a number
    let rules = [
      v => v != null ? true : 'Value is required',
      v => isValidNumber(v) || 'Must be a number'
    ]
    return rules
  })
  const percentageRules = computed(() => {
    // array with two rules, second rule checks if value is a number
    let rules = [
      v => v != null ? true : 'Value is required',
      v => isValidNumber(v) || 'Must be a number',
      v => v >= 0 && v <= 100 || 'Must be between 0 and 1'
    ]
    return rules
  })
  const numberIfNotNullRules = computed(() => {
    // array with two rules, second rule checks if value is a number
    let rules = [
      v => {
        if (v === null)
          true
        else
          isValidNumber(v) || 'Must be a number'
      }
    ]
  })
  const reverse = (arr) => arr.slice().reverse()
  return {
    nameRules, startDateRules, endDateRules, numberRules, percentageRules,
    reverse, numberIfNotNullRules
  }
}

export function useEnviroForm ({createFunc, createState, params}){
  const every_nth = (arr, nth) => arr.filter((e, i) => i % nth === nth - 1)
  const getOrCreate = () => {
    createState = useAsyncState(
      createFunc({
        params: params.value,
      }),
      {},
      {
        onError: (error) => {
          console.error(error.response)
        }
      }
    )
    return createState
  }
  return {
    getOrCreate,
    every_nth
  }
}

export function useForecastForm ({
  blocks, initial, mean, volatility, model, 
  createFunc,
  createState,
  }){
  const globalState = useGlobalStateStore()
  const models = globalState.allowedTimeSeriesModels
  
  const createParams = computed (() => {
    return {
      blocks: blocks, // blocks is not a ref
      initial: initial.value,
      mean: mean.value,
      volatility: volatility.value,
      model: model.value
    }
  })
  const enviroForm = useEnviroForm({
      createFunc, 
      createState, 
      params: createParams
    })
  
  watchEffect(() => {
    if ( model.value === 'Constant' ) {
      mean.value = null
      volatility.value = null
    } else if ( model.value === 'CGR' ) {
      volatility.value = null
    }
  })
  return {
    initial, mean, volatility, model, models, createState, enviroForm
  }
}

export class TableMaker {
  /* 
  
  */
  constructor(potentialCols, statColumns=null, periodParams={}) {
    this.requiredAttrs = { 
      'bodyClass': null, 
      'component': false,
      'bodyFunc': false,
      'editor': false, 
      'filter': false,
      'frozen': false,
      'hidden': false,
      'spanWrap': false,
    }
    this.columns = []

    this.pushBaseColumns(potentialCols, statColumns)
    this.attachRequiredAttrs()

    if (statColumns !== null) {
      const periodCols = statColumns.slice(this.columns.length)   
      this.periodParams = periodParams
      if (periodCols !== null)
        this.pushPeriodColumns(periodCols)
        this.attachPeriodAttrs(periodCols)
    }
  }
  pushBaseColumns (potentialCols, statColumns) {
    potentialCols.forEach(col => {
      if (statColumns === null)
        this.columns.push(col)
      else
        if (statColumns.includes(col.field)) {
            this.columns.push(col)
        }
    })
  }
  pushPeriodColumns (periodCols){
    periodCols.forEach(header => {
      this.columns.push({
        field: header,
        header: header,
        sortable: true,
      })
    })
  }
  attachRequiredAttrs() { 
    this.columns.forEach((field) => {
      Object.entries(this.requiredAttrs).forEach(entries => {
        var [k, v] = entries
        if (!(k in field)) {
          field[k] = v
        }
      })
    })
  }
  periodAttrs () {
    var base = {
      bodyFunc: (data, field) => format.currency(data[field]),
      sortable: false
    }    
    for (const [key, value] of Object.entries(this.periodParams)) {
      base[key] = value
    }
    return base
  }  
  attachPeriodAttrs(periodCols) {
    this.columns.forEach((field) => {
      if (periodCols.includes(field.field)) {
        Object.entries(this.periodAttrs(periodCols)).forEach(entries => {
          var [k, v] = entries
          if (!(k in field)) {
            field[k] = v
          }
        })
      }
    })
  }
}

export class NewTableMaker {
  /* 
  
  */
  constructor({columns, otherHeaders, headerParams}) {
    this.requiredAttrs = { 
      'bodyClass': null, 
      'component': false,
      'bodyFunc': false,
      'editor': false, 
      'filter': false,
      'frozen': false,
      'hidden': false,
      'spanWrap': false,
      'sortable': false,
    }
    this.columns = []
    columns.forEach(col => {
      this.columns.push(col)
    })

    if (otherHeaders) {
      this.headerParams = headerParams
      this.pushHeaderColumns(otherHeaders)
      this.attachHeaderAttrs(otherHeaders)
    }
    this.attachRequiredAttrs()
  }
  pushHeaderColumns (headers){
    headers.forEach(header => {
      this.columns.push({
        field: header,
        header: header,
      })
    })
  }
  attachRequiredAttrs() { 
    this.columns.forEach((field) => {
      Object.entries(this.requiredAttrs).forEach(entries => {
        var [k, v] = entries
        if (!(k in field)) {
          field[k] = v
        }
      })
    })
  }
  // periodAttrs () {
  //   var base = {
  //     sortable: false
  //   }    
  //   for (const [key, value] of Object.entries(this.periodParams)) {
  //     base[key] = value
  //   }
  //   return base
  // }  
  attachHeaderAttrs(headers) {
    this.columns.forEach((field) => {
      if (headers.includes(field.field)) {
        Object.entries(this.headerParams).forEach(([k,v]) => {
          if (!(k in field)) {
            field[k] = v
          }
        })
      }
    })
  }
}

export function useObjectManager ({store}) {

  const { state, isReady, isLoading, error, execute } = useAsyncState(() => store.getObjects())

  const saveState = ref(null)
  const save = () => {
    saveState.value = useAsyncState(() => store.updateObjects())
  }

  const objects = ref([])
  watchEffect(() => {
    if (isReady.value) {
      objects.value = store.objects
    }``
  })
  const { history, undo, redo } = useRefHistory(objects, {deep: true})

  watch(objects, (newVal, oldVal) => {
    store.setObjects(newVal)
  })
  return { objects, isReady, isLoading, error, execute, save, saveState, history, undo, redo}
}