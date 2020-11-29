import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios"
import "bootstrap"
import 'leaflet/dist/leaflet.css';


import VueApexCharts from 'vue-apexcharts'


Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)



const store = Vue.observable({ authenticated: false, user: "",  state: "user", token: "", primary_color: "#111111" , secondary_color: "#666777",
 setToken(token){
  localStorage.setItem("token", token)
  this.authenticated = true
} })

let token = localStorage.getItem("token");

if(token == "" || !token){
  store.token = token;
  store.authenticated = false
}else{
  store.token = token;
  store.authenticated = true
}


Vue.prototype.$store = store
Vue.prototype.$axios = axios



Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
