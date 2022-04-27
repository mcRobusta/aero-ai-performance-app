import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import VueFrappe from 'vue2-frappe';
import Vuesax from 'vuesax'
import 'vuesax/dist/vuesax.css' //Vuesax styles
import 'material-icons/iconfont/material-icons.css'

Vue.use(Vuesax, {

})
Vue.use(VueFrappe)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
