<template>
    <v-app>
        <v-main>
            <navBar app v-if="shouldDisplayNavbar()" />
            <router-view />
        </v-main>
    </v-app>
</template>

<script>
    import navBar from './components/navigation-bar';
    import {
        baseUrl
    } from './BaseRequestUrl';
    const axios = require('axios');

    const delta = 14*60*1000;
   // setInterval(this.refreshTokens, delta);
    export default {
        name: "App",
        data: () => ({}),
        components: {
            navBar
        },
        methods: {
            shouldDisplayNavbar() {
                const path = this.$router.currentRoute.path;
                return path !== '/' && path !== '/register' && path !== '/login' && path !== '/dashboard' && path !== '/API';
            },

        async refreshTokens() {
        if(!localStorage.getItem('refresh_token')) {
            return;
        }
        const refresh_token = localStorage.getItem('refresh_token');
        const data =  {
          };
          const config = {
              method: 'get',
              url: baseUrl + '/refresh',
              data: data,
              headers: {
                Authorization: 'Bearer ' + refresh_token
            }
         };
        try {
        const res = await axios(config);
        localStorage.setItem('access_token',res.data['access']);
        localStorage.setItem('refresh_token',res.data['refresh']);
        console.log('new token: ' +  localStorage.getItem('refresh_token'));       
         }
         catch(err) {
            console.log(err);
         }

        },
        },
        created() {
            setInterval(this.refreshTokens, delta);
        }     
        
    };
</script>
