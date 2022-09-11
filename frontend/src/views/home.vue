<template>
<v-app-bar
  elevation="4" 
>
<v-toolbar-title class="black--text">Sign Language API</v-toolbar-title>
<v-spacer></v-spacer>
      <v-btn
        color="black"
        class="mr-4 white--text"
        @click="goToRegister()"
      >
        Register
      </v-btn>

      <v-btn
        color="black"
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
