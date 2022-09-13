<template>
    <v-container>

    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model="name"
        :counter="10"
        :rules="nameRules"
        label="Name"
        required
      ></v-text-field>
  
      <v-text-field
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required
      ></v-text-field>
  
  
      <v-btn
        :disabled="!valid"
        color=#17252A
        class="mr-4 white--text"
        @click="validate"
      >
        Register
      </v-btn>
  
    </v-form>
</v-container>
  </template>

<script>
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
        
      }),
  
      methods: {
        validate () {
          this.$refs.form.validate()
        },
      },
    }
  </script>