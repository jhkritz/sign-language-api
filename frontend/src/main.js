import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAuth from 'vue-auth'

import home from './views/home'
import addsign from './views/addsign'
import library from './views/library'
import PageNotFound from './views/PageNotFound';
import UploadLibrary from './views/UploadLibrary';

Vue.config.productionTip = false

const routes = [

	{
		path: '/',
		name: 'home',
		component: home
	},
	{
		path: '/library/upload',
		component: UploadLibrary
	},
	{
		path: '/library/:id',
		name: 'library',
		component: library,
	},
	{
		path: '/addsign',
		name: 'addsign',
		component: addsign,
	},
	{
		path: '/:pathMatch(.*)*',
		component: PageNotFound
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
