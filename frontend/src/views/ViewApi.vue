<template>
    <v-container>
        <h1>
            Your current API Key is :
        </h1> 
        <br/>
        <p class="font-weight-regular">
            {{APIkey}}
        </p>
        <h3>
            Click here to generate your API key (note that this will deactivate any previous API keys):
        </h3>
        <br/>
        <v-btn
            color=#17252A
            class="mr-4 white--text"
            @click="UpdateApi"
        >
            Update API Key
        </v-btn>
        <br/>
        <br/>
        <br/>
        <v-btn
            color=#17252A
            class="mr-4 white--text"
            @click="goToDashboard"
        >
            Done
        </v-btn>
    </v-container>
</template>

<script>
import { sharedState } from '../SharedState';
import {
    baseUrl
} from '../BaseRequestUrl.js';

const axios = require('axios');
export default {
    data: () => ({
        APIkey: sharedState.API_key
    }),
    methods: {
        goToDashboard(){
            this.$router.push("/dashboard");
        },
        async UpdateApi(){
            try {
                const config = {
                    method: 'get',
                    url: baseUrl + '/api/resetapikey',
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                // Get list of libraries
                const res = await axios(config);
                this.APIkey = res.data['api_key'];
                console.log(res.data['api_key']);
            } catch (err) {
                console.error(err);
            }
        }
    },
}
</script>
