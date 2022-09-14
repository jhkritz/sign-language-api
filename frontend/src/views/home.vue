<style>
.bg {
  position: fixed;
  top: 0px;
  left: 0;
  z-index: 999;
  width: 100%;
  height: 100vh;
  text-align: center;

  background-image: url('../assets/bg-poly.svg');
  background-attachment: scroll;
  background-size: cover;
  background-position: left, top;
}

.bar {
  backdrop-filter: blur(0px);
  font-family: Arial, Helvetica, sans-serif;
}

.main-text {
  text-align: left;
  margin-top: 12vh;
  margin-left: 5vh;
  color: white;
  font-family: Arial, Helvetica, sans-serif;

}

.bigtext {
  display: block;
  font-size: 3em;
  margin-left: 0;
  margin-right: 0;
  font-weight: bold;
}

.desc {
  margin-top: 0.67em;
  margin-bottom: 0.33em;
  font-size: 1.5em;
  width: 45vw;
}
</style>

<template>
  <div class="bg">
    <v-app-bar elevation="0" color=transparent class="bar">
      <v-toolbar-title class="white--text">Sign Language API</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color=#17252A class="mr-4 white--text" @click="goToRegister()">
        Register
      </v-btn>

      <v-btn color=#17252A class="mr-4 white--text" @click="goToLogin()">
        Login
      </v-btn>
    </v-app-bar>

    <div class="main-text">
      <h1 class="bigtext">Welcome, </h1>
      <h1 class="bigtext">to the Sign Language API.</h1>
      <p class="desc">
        Discover how you can start using image based sign language recognition in your projects today, by signing up for
        API usage.
      </p>
      <div style="padding-top: 1.5em"></div>
      <v-btn rounded x-large color=#17252A class="mr-4 white--text" @click="goToRegister()">
        Register
      </v-btn>
      <v-btn rounded x-large color=#17252A class="mr-4 white--text" @click="goToLogin()">
        Login
      </v-btn>
    </div>


  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  setup() {

  },
  methods: {
    goToRegister() {
      this.$router.push('/register');
    },
    goToLogin() {
      this.$router.push('/login');
    },
  },
})
</script>
