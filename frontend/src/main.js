import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAuth from 'vue-auth'

import home from './views/home'
import addsign from './views/addsign'
import page_not_found from './views/page-not-found';
import test_library from './views/test-library';
import explore_library from './views/explore-library';

Vue.config.productionTip = false

const routes = [{
		path: '/',
		name: 'home',
		component: home
	},
	{
		path: '/library',
		component: explore_library,
		props: route => ({
			library_id: route.query.library_id
		})
	},
	{
		path: '/library/test',
		component: test_library,
		props: {
			lib_name: 'test_library'
		}
	},
	/*
	{
		path: '/library',
		component: library,
		props: route => ({
			library_id: route.query.library_id
		})
	},*/
	{
		path: '/addsign',
		component: addsign,
		props: route => ({
			library_id: route.query.library_id
		})
	},
	{
		path: '/:pathMatch(.*)*',
		component: page_not_found
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
}).$mount('#app');
