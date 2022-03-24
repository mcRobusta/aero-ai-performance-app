<template>
  <div id="app">

    <vs-row vs-type="flex" vs-justify="center" vs-align="center" vs-w="12"> 
    <!-- Flight details -->
      <vs-col  vs-w="3">
        <vs-input
        label-placeholder="Flight Number"
        v-model="flightNo"/>
      </vs-col>
      <vs-col vs-w="3">
        <vs-input
        label-placeholder="Origin"
        v-model="originAirport"/>
      </vs-col>
      <vs-col vs-w="3">
        <vs-input
        label-placeholder="Destination"
        v-model="destinationAirport"/>
      </vs-col>
    </vs-row>

    <br>
    <br>

    <vs-button @click="printData">
    </vs-button>

    <vs-row vs-w="12" vs-type="flex" vs-justify="flex-start">
    <!-- Inputs -->
      <vs-col vs-w="3" vs-offset="1.5">
        <div
        v-for="(field) in inputList" 
        :key="field.field"
        vs-type="flex" 
        vs-justify="center">

          <div v-if="field.type == 'numeric'">
            {{ field.field }}
            <!-- <vs-input 
            :label-placeholder="field"
            :v-model="value">
            </vs-input> -->
            <vs-input-number v-model="field.value" :min="field.min" :max="field.max" :step="field.step"/>
            {{ field.value + field.unit }}
          </div>

          <div v-if="field.type == 'numeric-text'">
            <vs-input
              border
              type="number"
              v-model="field.value"
              :label="field.field"
            />
          </div>

          <div v-if="field.type == 'boolean'">
            {{ field.field }}
            <vs-switch v-model="field.value">
              <span slot="on">{{ field.on }}</span>
              <span slot="off">{{ field.off }}</span>
            </vs-switch>
          </div>

          <div v-if="field.type == 'numeric-slider'">
            {{ field.field }}
            <vs-slider v-model="field.value" :step="field.step" :max="field.max"/>
            <div>
              {{ field.value + field.unit }}
            </div>
          </div>

          <br>
        </div>
      </vs-col>
    <!-- Outputs -->
      <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="3">
        <p>Outputs</p>
      </vs-col>
    </vs-row>

  </div>
</template>

<script>
const fs = require('fs');
export default {
  name: 'App',
  data:() => ({
        flightNo: '',
        originAirport: '',
        destinationAirport: '',
        inputList: [
          {'field': 'Temperature', 'type': 'numeric-text', 'value': 0, 'unit':'ºC', 'min': -20, 'max': 65},
          {'field':'Runway Length', 'type': 'numeric', 'value': 1500, 'unit':'m', 'min': 1500, 'max':3000, 'step': 250},
          {'field':'Pressure Altitude', 'type': 'numeric-slider', 'value': 0, 'unit':'FT', 'max': 2002, 'step': 1000},
          {'field':'Max Takeoff Weight', 'type': 'numeric-text', 'value': 0, 'unit':'1000KG', 'min': 40, 'max': 80, 'step': 0.1}
        ],
        outputList: {
          'wind': 0,
          'temp': 0,
          'qnt': 0,
          'anti-ice': false,
          'cog>27': false,
          'thrust': false
        },
      }),
  methods: {
    printData() {
      const datafile = require('./assets/datafile.json')
      console.log(datafile[0])
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.center {
  margin: auto;
  display: flex;
  align-items: center;
}
</style>
