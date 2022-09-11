<template>
<v-app-bar
  elevation="4" 
  color=#3AAFA9
>
<v-toolbar-title class="white--text">Sign Language API</v-toolbar-title>
<v-spacer></v-spacer>
      <v-btn
        color=#17252A
        class="mr-4 white--text"
        @click="goToRegister()"
      >
        Register
      </v-btn>

      <v-btn
        color=#17252A
        class="mr-4 white--text"
        @click="goToLogin()"
      >
        Login
      </v-btn>
</v-app-bar>  
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  setup() {
    
  },
  methods:{
  goToRegister(){
    this.$router.push('/register');
  },
  goToLogin(){
    this.$router.push('/login');
  },
  },
})
</script>
