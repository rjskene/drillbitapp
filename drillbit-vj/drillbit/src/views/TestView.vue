<script setup>
import { ref, computed } from 'vue'

const value = ref(22222)

const humanFormat = (number) => {
  if (isNaN(number)) {
    number = ""
  } else {
    // number = Number(number).toLocaleString(this.options.locale, {maximumFractionDigits: 2, minimumFractionDigits: 2, style: 'currency', currency: 'BRL'});
    number = Number(number).toLocaleString('en-US', {
      maximumFractionDigits: 2,
      minimumFractionDigits: 2
    });
  }
  console.log(number)
  return number
}
const isInteger = (value) => {
  let result = false;
  if (Number.isInteger(parseInt(value))) {
    result = true;
  }
  return result;
}
const cleanNumber = (value) => {
  let result = "";
  if (value) {
    let flag = false;
    let arrayValue = value.toString().split("");
    for (var i = 0; i < arrayValue.length; i++) {
      if (isInteger(arrayValue[i])) {
        if (!flag) {
          // Retirar zeros à esquerda
          if (arrayValue[i] !== "0") {
            result = result + arrayValue[i];
            flag = true;
          }
        } else {
          result = result + arrayValue[i];
        }
      }
    }
  }
  return result
}
const valueWhenIsEmpty = ref("")
const machineFormat = (number) => {
  if (number) {
    number = cleanNumber(number);
    // Ajustar quantidade de zeros à esquerda
    number = number.padStart(parseInt(options.precision) + 1, "0");
    // Incluir ponto na casa correta, conforme a precisão configurada
    number =
      number.substring(
        0,
        number.length - parseInt(options.precision)
      ) +
      "." +
      number.substring(
        number.length - parseInt(options.precision),
        number.length
      );
    if (isNaN(number)) {
      number = valueWhenIsEmpty;
    }
  } else {
    number = valueWhenIsEmpty;
  }
  if (options.precision === 0) {
    number = cleanNumber(number);
  }
  return number;
}
const cmpValue = computed({
  get: function() {
    console.log(value.value, value.value !== null && value.value !== "", humanFormat(value))
    return value.value !== null && value.value !== ""
      ? humanFormat(value.value.toString())
      : valueWhenIsEmpty;
  },
  set: function(newValue) {
    value.value = newValue
    // $emit("input", this.machineFormat(newValue));
  }
})

</script>

<template>
  <v-text-field
    v-model="cmpValue"
    prefix="$"
  />
    human {{ humanFormat(value) }}
    clean {{ cleanNumber(value) }}
    {{ value }}
    {{ cmpValue }}
</template>

  
  
<style scoped>
  
</style>