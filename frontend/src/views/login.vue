<template>
  <v-app>
    <div>
      <!--Navigation bar-->
      <v-app-bar 
      elevation="0" 
      color=#3AAFA9>
        <v-appbar-title 
        class="white--text">Sign Language API
        </v-appbar-title>
        <v-spacer>
        </v-spacer>
        <v-btn 
        icon color="white" 
        id='homeButton' 
        to='/'>
          <v-icon>mdi-home</v-icon>
        </v-btn>
      </v-app-bar>
    </div>
    <!--Login form-->
    <v-container 
        fill-height>
        <v-layout 
        align-center 
        justify-center>
      <v-form 
      ref="form" 
      v-model="valid" 
      lazy-validation>
      <center>
      <h1 class = "pb-8" >
      Log in
        </h1>
      </center>
        <v-text-field 
        outlined
        v-model="email" 
        :counter="40" 
        :rules="emailRules" 
        label="Email" 
        required>
        </v-text-field>

        <v-text-field 
        outlined
        v-model="password" 
        type="password" 
        :rules="passRules" 
        label="Password" 
        required>
        </v-text-field>
        <v-btn 
        :disabled="!valid" 
        color=#17252A 
        class="mr-4 white--text" 
        @click="postInfo()">
          Log In
        </v-btn>
      </v-form>
        </v-layout>
    </v-container>
  </v-app>
</template>
  
<script>

import {
  baseUrl
} from '../BaseRequestUrl';
const axios = require('axios');
export default {
  data: () => ({
    valid: true,
    email: "",
    emailRules: [
      (v) => !!v || "E-mail is required",
      (v) => /.+@.+/.test(v) || "E-mail must be valid",
    ],
    password: "",
    passRules: [(v) => !!v || "Password is required"],
    singleSelect: 0,
    value: ""
  }),

  methods: {
    goToHome() {
      this.$router.push("/");
    },
    async postInfo() {
      const data = {
        email: this.email,
        password: this.password
      };
      const config = {
        method: 'post',
        url: baseUrl + '/login',
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
          this.$router.push("/dashboard");

        }
        else {
          alert('Incorrect email or password')
        }
      } catch (err) {
        alert('Incorrect email or password')
        console.error(err);
      }
    },
  },
};
</script>
  
<style scoped>
form {
  max-width: 320px;
  margin: 30px auto;
  background: whitesmoke;
  text-align: left;
  padding: 40px;
  border-radius: 10px;
}

button {
  width: 200px;
  padding: 15px 0;
  text-align: center;
  margin: 20px 10px;
  border-radius: 25px;
  font-weight: bold;
  border: 2px solid black;
  color: grey;
}
</style>

<style scoped>
.logo {
  width: 7%;
  margin-left: 1%;
}
</style>