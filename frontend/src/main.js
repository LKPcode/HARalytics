import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios"
import "bootstrap"
import 'leaflet/dist/leaflet.css';


import VueApexCharts from 'vue-apexcharts'


Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)



const store = Vue.observable({ authenticated: false, user: "",  state: "", token: "", email:"",
 setToken(res){
  localStorage.setItem("token", res.token)
  localStorage.setItem("user", res.user)
  localStorage.setItem("state", res.state)
  localStorage.setItem("email", res.email)

  this.authenticated = true
  this.token = token
},
  logout(){
    localStorage.setItem("token", "")
    localStorage.setItem("email", "")

    
    localStorage.setItem("user", "")
    localStorage.setItem("state", "")
    this.authenticated = false
    this.token = ""
  }
})

let token = localStorage.getItem("token");
store.user = localStorage.getItem("user");
store.state = localStorage.getItem("state");
store.email = localStorage.getItem("email");

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
