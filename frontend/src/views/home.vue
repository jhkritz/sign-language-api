<style>
.bg {
  position: absolute;
  top: 0px;
  left: 0;
  z-index: 999;
  width: 100%;
  height: 180vh;
  overflow: scroll;

  background-image: url('../assets/bg-poly.svg');
  background-attachment: fixed;
  background-size: cover;
  background-position: left, top;
}

.bar {
  backdrop-filter: blur(0px);
  font-family: Arial, Helvetica, sans-serif;
}

.main-text {
  text-align: left;
  margin-top: 3vh;
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

.features {
  width: 100%;
  align-content: space-between;
  display: flex;
  margin-top: 5vh;
  margin-left: 5vh;
  flex-wrap: wrap;
  flex-direction: row;
  gap: 2vw;
}

.frosted {
  font-family: Arial, Helvetica, sans-serif;
  background-color: #4D949B;
  max-width: 20em;
  max-height: 20em;
  min-width: 20em;
  min-height: 5em;
  backdrop-filter: blur(40px) hue-rotate(0deg);
}
</style>

<template>
  <div class="bg">
    <v-app-bar elevation="0" color=transparent class="bar">
      <!--v-toolbar-title class="white--text">Sign Language API</v-toolbar-title-->
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

    <div class="features">

      <v-card color=#4D949B dark shaped class="frosted" elevation="15">
        <v-icon large style="padding:0.8vw">mdi-folder-multiple-image</v-icon>
        <v-card-title class="text-h5">
          Custom image libraries
        </v-card-title>

        <v-card-subtitle>Create custom image libraries that are trained on sign data you supply.
        </v-card-subtitle>
      </v-card>

      <v-card color=#4D949B dark shaped class="frosted" elevation="15">
        <v-icon large style="padding:0.8vw">mdi-hand-wave</v-icon>
        <v-card-title class="text-h5">
          Train individual signs
        </v-card-title>

        <v-card-subtitle>Capture and label hand signs for training straight from your webcam!
        </v-card-subtitle>
      </v-card>

    </div>

    <div class="features">

      <v-card color=#4D949B dark shaped class="frosted" elevation="15">
        <v-icon large style="padding:0.8vw">mdi-zip-box</v-icon>
        <v-card-title class="text-h5">
          Bulk file uploads
        </v-card-title>

        <v-card-subtitle>Bulk upload a labelled image dataset for training.
        </v-card-subtitle>
      </v-card>

      <v-card color=#4D949B dark shaped class="frosted" elevation="15">
        <v-icon large style="padding:0.8vw">mdi-code-tags</v-icon>
        <v-card-title class="text-h5">
          API usage
        </v-card-title>

        <v-card-subtitle>Apply for an API key to use your trained datasets in your own projects.
        </v-card-subtitle>
      </v-card>

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
