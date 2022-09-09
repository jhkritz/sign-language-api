<template>
    <v-app>
      <v-row>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="email"
            :counter="40"
            :rules="emailRules"
            label="Email"
            required
          ></v-text-field>
  
          <v-text-field
            v-model="password"
            type="password"
            :rules="passRules"
            label="Password"
            required
          ></v-text-field>
          <v-btn :disabled="!valid" color="black" class="mr-4 white--text" @click="login()">
            Log In
          </v-btn>
        </v-form>
      </v-row>
    </v-app>
  </template>
  
  <script>
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