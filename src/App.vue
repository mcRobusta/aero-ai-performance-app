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
        <vs-select label="Origin Airport" v-model="takeoffRunway" @change="computeV()">
          <vs-select-item v-for="airport in airportList" :key="airport.code" :text="airport.name" :value="airport.runwayLength">
            {{airport.name}}
          </vs-select-item>
        </vs-select>
      </vs-col>
      <vs-col vs-w="3">
        <vs-select label="Destination Airport">
          <vs-select-item v-for="airport in airportList" :key="airport.name" :text="airport.name">
            {{airport.name}}
          </vs-select-item>
        </vs-select>
      </vs-col>
    </vs-row>

    <br>
    <br>

    <vs-button @click="computeV()">
      Calculate values
    </vs-button>

    <br>
    <br>

    <!--
    <div>
        Temperature / Pressure
        <vs-switch v-model="dummyVModel" @change="inputToggle()">
          <span slot="on">Temperature</span>
          <span slot="off">Altitude</span>
        </vs-switch>
    </div>
    -->

    <vs-row vs-w="12" vs-type="flex" vs-justify="flex-start">
    <!-- Inputs -->
      <vs-col vs-w="3" vs-offset="1">
        <vs-card class="inputCard" fixed-height style="background-color: #dedede">

          <div slot="header">
            Inputs
          </div>

          <div
          v-for="(field) in inputList" 
          :key="field.field"
          vs-type="flex" 
          vs-justify="center">

            <div v-if="field.type == 'numeric' && field.enabled">
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
              <vs-switch v-model="field.value" @change="computeV()">
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
      </vs-card>
    </vs-col>
    <!-- Outputs -->
    <vs-col vs-w="3" vs-offset="4">
      <vs-card class="inputCard" fixed-height style="background-color: #222222">

        <div slot="header">
          Outputs
        </div>

        <div
        v-for="(field) in outputList" 
        :key="field.field"
        vs-type="flex" 
        vs-justify="flex-end">
          <p v-if="field.enabled">{{ field.field + ': ' + field.value + field.unit }}</p>
        </div>
      </vs-card>
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
        takeoffRunway: 3316,
        dummyVModel: false,
        airportList: [
          {'name': 'London Gatwick', 'code': 'EGKK 08R/26L', 'runwayLength': 3316},
          {'name': 'London Heathrow', 'code': 'EGLL 09L/27R', 'runwayLength': 3201},
          // Note! London Heathrow's runway length was changed from 3901 to 3201 to fit given data.
          {'name': 'Manchester', 'code': 'EGCC 05R/23L', 'runwayLength': 3050}
        ],
        inputList: [
          {'field': 'Temperature', 'type': 'numeric', 'value': 0, 'unit':'ºC', 'min': -20, 'max': 65, 'enabled': true},
          {'field': 'Pressure', 'type': 'numeric', 'value': 0, 'unit':'hPa', 'enabled': false},
          {'field': 'Altitude', 'type': 'numeric-slider', 'value': 0, 'unit':'FT', 'max': 2002, 'step': 1000, 'enabled': true},
          {'field':'Engine Anti-ice', 'type': 'boolean', 'value': false, 'on': "ON", "off": "OFF", 'enabled': true},
          {'field':'Total Anti-ice', 'type': 'boolean', 'value': false, 'on': "ON", "off": "OFF", 'enabled': true},
          {'field':'Air Conditioning', 'type': 'boolean', 'value': false, 'on': "ON", "off": "OFF", 'enabled': true},
          {'field':'FLEX / Full-thrust Takeoff', 'type': 'boolean', 'value': false, 'on': "Full-thrust", "off": "FLEX", 'enabled': true},
        ],
        outputList: [
          {'field': 'V1', 'value': 122, 'unit':'Kt', 'enabled': true},
          {'field': 'Vr', 'value': 122, 'unit':'Kt', 'enabled': true},
          {'field': 'V2', 'value': 127, 'unit':'Kt', 'enabled': true},
          {'field': 'Pressure', 'value': 1000, 'unit':'hPa', 'enabled': false},
          {'field': 'Temperature', 'value': 0, 'unit':'hPa', 'enabled': false},
          {'field':'Max Takeoff Weight', 'value':65.2, 'unit':' metric tonnes', 'enabled': true}
        ],
      }),
  methods: {
    printData() {
      this.computeV()
    },

    inputToggle() {
      this.inputList[0].enabled = !this.inputList[0].enabled
      this.inputList[1].enabled = !this.inputList[1].enabled
      this.outputList[0].enabled = !this.outputList[0].enabled
      this.outputList[1].enabled = !this.outputList[1].enabled
      this.outputList.push(0)
      this.outputList.pop()
    },

    searchDatafile(runway, pressureAltitude) {
      /* 
         Search the Python-generated datafile
         for entries that fit within the user 
         inputs. Return the results as an array.
      */
      var validEntries = [];
      const runway_lowerBound = Math.round(runway / 1000) * 1000
      const runway_upperBound = runway // Obviously, the longest runway length we should pick should be less than or equal to the actual runway.
      for (var i = 0; i < datafile.length; i++) {
        var currentEntry = datafile[i];
        var searchParameters = 
          pressureAltitude == currentEntry.pressureAltitude &&
          (currentEntry.runwayLengths >= runway_lowerBound && currentEntry.runwayLengths <= runway_upperBound);
        if (searchParameters) {
           validEntries.push(currentEntry);
        }
      }
      return validEntries;
    },
    
    extractArray(filteredArray, name) {
      /*
        Extracts field values (e.g. "temperature")
        from the filtered array and returns them
        as an easy-to-use 1D array.
      */
      let extractedArray = []
      for (let index = 0; index < filteredArray.length; index++) {
        extractedArray.push(filteredArray[index][name])
      }
      return extractedArray
    },

    graphFunction(xArray, yArray, value) {
      for (var i = 0; i < xArray.length - 1; i++) {
        if (value >= xArray[i] && value <= xArray[i + 1]) {
          const gradient = (yArray[i + 1] - yArray[i]) / (xArray[i + 1] - xArray[i])
          var interpolatedValue = gradient * value
          interpolatedValue += yArray[i]
          return interpolatedValue
        }
      }
      if (value < xArray[0]) {
        return yArray[-1]
      } else {
        return yArray[0]
      }
    },

    thresholdChecks(v, p, type) {
      if (type == "1") {
        if (v < 112 && p < 0) {
          return 112;
        } else if (v < 111 && p < 1000) {
          return 111;
        } else if (v < 110 && p < 2000) {
          return 110;
        } else if (v < 109 && p < 3000) {
          return 109;
        } else if (v < 108 && p < 5000) {
          return 108;
        } else if (v < 107 && p < 6000) {
          return 108;
        } else if (v < 106 && p < 7000) {
          return 107;
        } else {
          return v;
        }
      }
    },

    computeV() {
      var filteredArray = this.searchDatafile(
        this.takeoffRunway,
        this.inputList[2].value
      )
      var maxToW = 0
      var temperature = 0
      if (this.inputList[6].value) { // If full-thrust takeoff:
        if (this.inputList[3].value) { // If engine anti-ice is on:
          maxToW -= 0.25
        }
        if (this.inputList[4].value) { // If total anti-ice is on:
          maxToW -= 0.75
        }
        if (this.inputList[5].value) { // If air conditioning is on:
          maxToW -= 2.2
        }
      } else {
        if (this.inputList[3].value) { // If engine anti-ice is on:
          temperature -= 1
        }
        if (this.inputList[4].value) { // If total anti-ice is on:
          temperature -= 2
        }
        if (this.inputList[5].value) { // If air conditioning is on:
          temperature -= 5
        }
      }
      const temperatureArray = this.extractArray(filteredArray, "temperature")
      temperature += parseFloat(this.inputList[0].value) // Vuesax takes numeric input as string, so conversion necessary.
      console.log(temperature)
      const v_1Array = this.extractArray(filteredArray, "v_1")
      const v_rArray = this.extractArray(filteredArray, "v_r")
      const v_2Array = this.extractArray(filteredArray, "v_2")
      const maxToW_array = this.extractArray(filteredArray, "maxToW")
      var v_1 = this.graphFunction(temperatureArray, v_1Array, temperature)
      var v_r = this.graphFunction(temperatureArray, v_rArray, temperature)
      var v_2 = this.graphFunction(temperatureArray, v_2Array, temperature)
      maxToW += this.graphFunction(temperatureArray, maxToW_array, temperature)
      this.outputList[0].value = this.thresholdChecks(v_1, this.inputList[2].value, "1")
      this.outputList[1].value = Math.round(v_r * 10) / 10
      this.outputList[2].value = Math.round(v_2 * 10) / 10
      this.outputList[3].value = Math.round(maxToW * 10) / 10
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
.inputCard {
  color: #00bfff;
}
</style>
