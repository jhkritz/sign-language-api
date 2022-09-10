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
import interpret_sign from './views/interpret-sign';
import library from './views/library';
import register from './views/register';
import login from './views/login';
import dashboard from './views/dashboard';
import {
	sharedState
} from './SharedState';

Vue.config.productionTip = false;

const routes = [
	{
		path: '/dashboard',
		name: 'dashboard',
		component: dashboard
	},
	{
		path: '/register',
		name: 'register',
		component: register
	},
	{
		path: '/login',
		name: 'login',
		component: login
	},
	{
		path: '/',
		name: 'home',
		component: home
	},
	{
		path: '/library/explore',
		name: 'library',
		component: library,
		props: route => ({
			library_id: route.query.library_id
		})
	},
	{
		path: '/library/test',
		component: interpret_sign,
		props: route => ({
			library_id: route.query.library_id
		})
	},
	{
		path: '/library/test',
		component: test_library,
		props: route => ({
			library_id: route.query.library_id
		})
	},
	{
		path: '/library/addsign',
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
	baseURL: process.env.NODE_ENV === 'production' ?
		'http://rocky-taiga-14209.herokuapp.com' : 'http://127.0.0.1/8000/',
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

router.beforeEach((to, from, next) => {
	if (from.path === '/library/test') {
		sharedState.stopCamera();
	}
	next();
});

Vue.prototype.$axios = instance

Vue.use(VueAuth)
new Vue({
	router,
	vuetify,
	render: h => h(App),
	data: {
		sharedState: sharedState
	},
}).$mount('#app');
