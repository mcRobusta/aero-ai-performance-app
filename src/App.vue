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

    <vs-button @click="computeV()">
      Calculate values
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
            <vs-input-number v-model="field.value" :min="field.min" :max="field.max" :step="field.step"  @input="computeV()"/>
            {{ field.value + field.unit }}
          </div>

          <div v-if="field.type == 'numeric-text'">
            <vs-input
              border
              type="number"
              v-model="field.value"
              :label="field.field"
              @change="computeV()"
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
            <vs-slider v-model="field.value" :step="field.step" :max="field.max"  @change="computeV()"/>
            <div>
              {{ field.value + field.unit }}
            </div>
          </div>

          <br>
        </div>
      </vs-col>
    <!-- Outputs -->
    <vs-col vs-w="3" vs-offset="1.5">
        <div
        v-for="(field) in outputList" 
        :key="field.field"
        vs-type="flex" 
        vs-justify="flex-end">
        <p>{{ field.field + ': ' + field.value + field.unit }}</p>
        </div>
      </vs-col>
    </vs-row>

  </div>
</template>

<script>
const datafile = require('./assets/datafile.json')

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
        ],
        outputList: [
          {'field': 'V1', 'value': 122, 'unit':'Kt'},
          {'field': 'Vr', 'value': 122, 'unit':'Kt'},
          {'field': 'V2', 'value': 127, 'unit':'Kt'},
          {'field':'Max Takeoff Weight', 'value':65.2, 'unit':'MG (megagram- 1000Kg)'}
        ],
      }),
  methods: {
    printData() {
      this.computeV()
    },
    searchDatafile(runway, pressureAltitude) {
      var validEntries = [];
      for (var i = 0; i < datafile.length; i++) {
        var dataEntry = datafile[i];
        var searchParameters = 
          pressureAltitude == dataEntry.pressureAltitude &&
          runway == dataEntry.runwayLengths;
        if (searchParameters) {
           validEntries.push(dataEntry);
        }
      }
      return validEntries;
    },
    filterArrays(arrayList, temperature) {
      var temperatureDistance = 100;
      var distance = 0;
      var primeIndex = 0;
      var primeIndexIsNegative = false;
      for (var i = 0; i < arrayList.length; i++) {
        var negativeIndex = false;
        distance = arrayList[i].temperature - temperature;
        if (distance < 0) {
          negativeIndex = true;
          distance *= -1;
        }
        if (distance < temperatureDistance) {
          temperatureDistance = distance;
          primeIndex = i;
          primeIndexIsNegative = negativeIndex;
        }
      }
      return [primeIndex, primeIndexIsNegative];
    },
    interpolateData(primeEntries, temperature){
      var temperature_0 = primeEntries[0].temperature;
      var temperature_1 = primeEntries[1].temperature;
      var inOrder = true;
      if (primeEntries[0].temperature > primeEntries[1].temperature) {
        temperature_0 = primeEntries[1].temperature;
        temperature_1 = primeEntries[0].temperature;
        inOrder = false;
      }
      console.log(temperature_0)
      console.log(temperature_1)
      var alpha = temperature - temperature_0;
      alpha /= temperature_1 - temperature_0;
      var lower_v_1 = primeEntries[0].v_1
      var lower_v_r = primeEntries[0].v_r
      var lower_v_2 = primeEntries[0].v_2
      var upper_v_1 = primeEntries[1].v_1
      var upper_v_r = primeEntries[1].v_r
      var upper_v_2 = primeEntries[1].v_2
      if (!inOrder) {
        lower_v_1 = primeEntries[1].v_1
        lower_v_r = primeEntries[1].v_r
        lower_v_2 = primeEntries[1].v_2
        upper_v_1 = primeEntries[0].v_1
        upper_v_r = primeEntries[0].v_r
        upper_v_2 = primeEntries[0].v_2
      }
      var v_1 = alpha * (upper_v_1 - lower_v_1) 
      v_1 += lower_v_1
      var v_r = alpha * (upper_v_r - lower_v_r) 
      v_r += lower_v_r
      var v_2 = alpha * (upper_v_2 - lower_v_2) 
      v_2 += lower_v_2
      return [v_1, v_r, v_2]
    },
    computeV() {
      var filteredArray = this.searchDatafile(
        this.inputList[1].value,
        this.inputList[2].value
      )
      var primeIndexArray = this.filterArrays(filteredArray, this.inputList[0].value);
      const primeIndex = primeIndexArray[0]
      const primeIndexIsNegative = primeIndexArray[1]
      var primeEntries = [ filteredArray[ primeIndex ] ]
      var maxToW = 0
      if ( primeIndexIsNegative ) {
        maxToW = filteredArray[primeIndex].maxToW
        if ( primeIndex > 0 ) {
          primeEntries.push( filteredArray[ primeIndex - 1 ] )
        } else {
          primeEntries.push( filteredArray[0] )
        }
      } else {
        maxToW = filteredArray[primeIndex + 1].maxToW
        if ( primeIndex < filteredArray.length ) {
          primeEntries.push( filteredArray[ primeIndex + 1] )
        } else {
          primeEntries.push( filteredArray[ filteredArray.length - 1 ] )
        }
      }
      const v_array = this.interpolateData(primeEntries, this.inputList[0].value);
      const v_1 = v_array[0]
      const v_r = v_array[1]
      const v_2 = v_array[2]
      this.outputList[0].value = v_1
      this.outputList[1].value = v_r
      this.outputList[2].value = v_2
      this.outputList[3].value = maxToW
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
