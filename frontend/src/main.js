import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAuth from 'vue-auth'
import ViewAPI from './views/ViewApi'
import dashboard from './views/dashboard'
import addsign from './views/addsign'
import page_not_found from './views/page-not-found';
import interpret_sign from './views/interpret-sign';
import library from './views/library';
import register from './views/register';
import login from './views/login';
import home from './views/home';
import API from './views/API';
import LibraryPermissionsPage from './views/LibraryPermissionsPage';
import temporary from './views/temporary';

import {
	sharedState
} from './SharedState';
import {
	baseUrl
} from './BaseRequestUrl';

Vue.config.productionTip = false;

const routes = [


	{
		path: '/temporary',
		name: 'temporary',
		component: temporary
	},
	
	{
		path: '/',
		name: 'home',
		component: home
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
		path: '/API',
		name: 'API',
		component: API,
		props: route => ({
			API_key: route.query.API_key
		})
	},
	{
		path: '/dashboard',
		name: 'dashboard',
		component: dashboard
	},
	{
		path: '/ViewApi',
		name: 'api',
		component: ViewAPI,
	},
	{
		path: '/library/permissions',
		name: 'permissions',
		component: LibraryPermissionsPage,
		props: route => ({
			library_id: route.query.library_id
		})
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
});

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

router.beforeEach(async (to, from, next) => {
	if (from.path.includes('/library/test') || from.path.includes('/addsign')) {
		sharedState.stopCamera();
	}
	if (!to.path.includes('login') && !to.path.includes('register') && to.path !==
		'/') {
		// Verify that the user is logged in.
		try {
			const url = new URL(baseUrl + '/verify/user');
			const config = {
				method: 'get',
				url: url,
				headers: {
					Authorization: 'Bearer ' + localStorage.getItem('access_token')
				}
			};
			await axios(config);
		} catch (err) {
			alert('Unauthorized.');
			console.log(err);
			router.push('/');
		}
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

axios.defaults.headers.common['Authorization'] =
	'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2MzA5OTE1MiwianRpIjoiMGJhY2JmNzItMTA4NS00M2E1LThmMDEtMWY5ZGE3N2YwMjdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTUsIm5iZiI6MTY2MzA5OTE1MiwiZXhwIjoxNjYzMTAwMDUyfQ.IFxLYf_Rr54nq4I7G1AVweeVOcswtwYyHB_EZld6LI8'
