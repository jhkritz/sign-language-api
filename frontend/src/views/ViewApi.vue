<template>
    <v-app>
        <div>
            <!--Navigation bar-->
            <v-app-bar elevation="0" color=#3AAFA9>
                <v-app-bar-title class="white--text">
                    Sign Language API
                </v-app-bar-title>
                <v-spacer>
                </v-spacer>
                <v-btn icon color="white" id='homeButton' @click="goToDashboard">
                    <v-icon>
                        mdi-home
                    </v-icon>
                </v-btn>
            </v-app-bar>
        </div>
        <v-container>
            <v-layout align-center justify-center>
            <v-sheet id='sheet' rounded="lg">
                <br>
                <br>
                <br>
                <br>
                        <center>
                        <h1>
                            Your current API Key is
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
                            Click here to view or in depth documentation on how to use our API
                        </h3>
                        <br />
                        <v-btn color=#17252A class="mr-4 white--text">
                            <a target="_blank" style="text-decoration: none; color: inherit;" href="../api_docs.html">API Documentation</a>
                        </v-btn>
                        <br />
                        <br />
                        <br />
                        </center>
            </v-sheet>
            </v-layout>
        </v-container>
</v-app>
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
