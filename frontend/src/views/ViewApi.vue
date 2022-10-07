<template>
    <v-main class="grey lighten-3" id='mainContainer'>
        <v-container>
            <v-sheet id='sheet' rounded="lg">
                <v-row id='row'>
                    <v-col lg='8' md='12'>
                        <h1>
                            Your current API Key is :
                        </h1>
                        <br />
                        <p class="font-weight-regular">
                            {{APIkey}}
                        </p>
                        <h3>
                            Click here to generate your API key (note that this will deactivate any previous API keys):
                        </h3>
                        <br />
                        <v-btn color=#17252A class="mr-4 white--text" @click="UpdateApi">
                            Update API Key
                        </v-btn>
                        <br />
                        <br />
                        <h3>
                            Add explanation here
                        </h3>
                        <br />
                        <v-btn color=#17252A class="mr-4 white--text">
                            <a href="../api_docs.html" style="text-decoration: none; color: inherit;">View Api Documentation</a>
                        </v-btn>

                        <br />
                        <br />
                        <br />
                    </v-col>
                </v-row>
            </v-sheet>
        </v-container>
    </v-main>
</template>

<script>
    import {
        sharedState
    } from '../SharedState';
    import {
        baseUrl
    } from '../BaseRequestUrl.js';

    const axios = require('axios');
    export default {
        data: () => ({
            APIkey: sharedState.API_key
        }),
        methods: {
            goToDashboard() {
                this.$router.push("/dashboard");
            },
            async UpdateApi() {
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
<style scoped>
    @media (max-width: 998px) {
        #sheet {
            width: 100%;
            padding: 2.5%;
            box-sizing: border-box;
            min-height: 60vh;
        }
    }

    @media (min-width: 1100px) {
        #sheet {
            width: 100%;
            padding: 2.5%;
            box-sizing: border-box;
            min-height: 75vh;
        }
    }
</style>
