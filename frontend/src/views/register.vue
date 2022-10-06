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
                <v-btn icon color="white" id='homeButton' to='/'>
                    <v-icon>
                        mdi-home
                    </v-icon>
                </v-btn>
            </v-app-bar>
        </div>
        <!--Registration form-->
        <v-container fill-height>
            <v-layout align-center justify-center>
                <v-form ref="form" v-model="valid" lazy-validation>
                    <center>
                        <h1 class="pb-8">
                            Create your account
                        </h1>

                    </center>
                    <v-text-field outlined v-model="email" :rules="emailRules" label="E-mail" required>
                    </v-text-field>

                    <v-text-field outlined v-model="password" :rules="passwordRules" :type="show1 ? 'text' : 'password'" name="input-10-1" label="Password" required>
                    </v-text-field>

                    <center>
                        <v-btn :disabled="!valid" color=#17252A class="mr-4 white--text" @click="postInfo()">
                            Register
                        </v-btn>
                    </center>

                </v-form>
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
    } from '../BaseRequestUrl';
    const axios = require('axios');
    export default {
        data: () => ({
            valid: true,
            email: '',
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            password: "",
            passwordRules: [
                (v) => !!v || "Password is required",
                (v) => v.length <= 20 || "Password must be less than 20 characters",
                (v) => v.length >= 5 || "Password must be more than 4 characters"
            ],
        }),

        methods: {
            validate() {
                this.$refs.form.validate()
            },
            async postInfo() {
                const data = {
                    email: this.email,
                    password: this.password
                };
                const config = {
                    method: 'post',
                    url: baseUrl + '/register',
                    data: data
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert('Success');
                        this.password = " ";
                        this.email = " ";
                        localStorage.setItem('access_token', res.data['access'])
                        localStorage.setItem('refresh_token', res.data['refresh'])
                        console.log(res.data['api_key']);
                        sharedState.setAPIkey(res.data['api_key']);
                        //this.$router.push(`/API?API_key=${res.data['api_key']}`);
                        this.$router.push('/dashboard');
                    } else {
                        alert(res.data)
                    }
                } catch (err) {
                    console.error(err);
                    alert('Registration failed.');
                }
            },


        },
    }
</script>
<style scoped>
    .logo {
        width: 7%;
        margin-left: 1%;
    }
</style>
