<template>
    <v-app>
        <v-main>
            <navBar app v-if="shouldDisplayNavbar()" />
            <router-view />
        </v-main>
    </v-app>
</template>

<style>
#sheet {
    width: 100%;
    padding: 2.5%;
    box-sizing: border-box;
    justify-content: space-between;
}

#mainContainer {
    height: 100%;
    box-sizing: border-box;
}

html {
    scrollbar-width: none;
    overflow-y: scroll;
}

::-webkit-scrollbar {
    display: none;
    width: 0;
    background: transparent;
}

#row {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    align-content: center;
    justify-content: center;
    margin: 0.5em;
    padding: 0.5em;
}
</style>

<script>
import navBar from './components/navigation-bar';
import {
    baseUrl
} from './BaseRequestUrl';
const axios = require('axios');
const delta = 13 * 60 * 1000;
export default {
    name: "App",
    data: () => ({}),
    components: {
        navBar
    },
    methods: {
        shouldDisplayNavbar() {
            const path = this.$router.currentRoute.path;
            return path !== '/' && path !== '/register' && path !== '/login' && path !== '/dashboard' && path !== '/API'&& path !== '/ViewApi';
        },

        async refreshTokens() {
            if (!localStorage.getItem('refresh_token')) {
                console.error('Missing refresh token.');
                return;
            }
            const refresh_token = localStorage.getItem('refresh_token');
            const data = {};
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
                localStorage.setItem('access_token', res.data['access']);
                localStorage.setItem('refresh_token', res.data['refresh']);
                console.log('access token' + localStorage.getItem('access_token'));
                console.log('new token: ' + localStorage.getItem('refresh_token'));
            } catch (err) {
                console.log(err);
            }

        },
    },

    created() {
        setInterval(this.refreshTokens, delta);
    }

};
</script>
