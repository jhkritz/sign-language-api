import Vue from 'vue'
import App from './App.vue'
//import router from './router'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAuth from 'vue-auth'

import HomeView from './views/HomeView'
import Libraries from './views/Libraries'

Vue.config.productionTip = false

const routes = [
  {
    path: '/',
    name: 'Home View',
    component: HomeView
  },
  {
    path: '/libraries',
    name: 'Libraries',
    component: Libraries
  },
]

Vue.use(VueRouter)

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
})

instance.interceptors.request.use(
  config => {
    let accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      config.headers = Object.assign({
        Authorization: accessToken
      }, config.headers);
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

const router = new VueRouter({
  mode: 'history',
  routes,
})

Vue.prototype.$axios = instance

Vue.use(VueAuth)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
