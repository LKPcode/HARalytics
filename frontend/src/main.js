import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios"
import "bootstrap"
import 'leaflet/dist/leaflet.css';


import VueApexCharts from 'vue-apexcharts'


Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)



const store = Vue.observable({ authenticated: false, user: "u",  state: "u", token: "", primary_color: "#111111" , secondary_color: "#666777",
 setToken(res){
  localStorage.setItem("token", res.token)
  localStorage.setItem("user", res.user)
  localStorage.setItem("state", res.state)
  this.authenticated = true
  this.token = token
},
  logout(){
    localStorage.setItem("token", "")
    
    localStorage.setItem("user", "")
    localStorage.setItem("state", "")
    this.authenticated = false
    this.token = ""
  }
})

let token = localStorage.getItem("token");
store.user = localStorage.getItem("user");
store.state = localStorage.getItem("state");
 store.token = token;
if(token == "" || !token){
  store.authenticated = false
}else{
  store.authenticated = true
}

Vue.prototype.$store = store
Vue.prototype.$axios = axios



Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
