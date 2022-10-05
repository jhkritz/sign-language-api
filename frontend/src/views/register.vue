<template>
    <v-app>
        <div>
            <!--Navigation bar-->
            <v-app-bar elevation="0" color=#3AAFA9>
                <!--v-appbar-title class="white--text">Sign Language API</v-appbar-title-->
                <v-spacer></v-spacer>
                <v-btn icon color="white" id='homeButton' to='/'>
                    <v-icon>mdi-home</v-icon>
                </v-btn>
            </v-app-bar>
        </div>
        <!--Registration form-->
        <v-container>
        <v-form ref="form" v-model="valid" lazy-validation>
            <!---- <v-text-field v-model="name" :counter="10" :rules="nameRules" label="Name" required></v-text-field> -->

            <v-text-field v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>

            <v-text-field v-model="password" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" :rules="passwordRules" :type="show1 ? 'text' : 'password'" name="input-10-1" label="Password" counter @click:append="show1 = !show1" required></v-text-field>

            <v-btn :disabled="!valid" color=#17252A class="mr-4 white--text" @click="postInfo()">
                Register
            </v-btn>

        </v-form>
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
            name: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
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
                        localStorage.setItem('access_token',res.data['access'])
                        localStorage.setItem('refresh_token',res.data['refresh'])
                        console.log(res.data['api_key']);
                        sharedState.setAPIkey(res.data['api_key']);
                        this.$router.push(`/API?API_key=${res.data['api_key']}`);
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