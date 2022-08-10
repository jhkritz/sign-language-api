<template>
    <v-container>
    <!--LIBRARY-->
    <h1>{{ $route.params.id }}</h1>
     <v-btn               
                depressed    
                @click="goto_addsign"
        >
        Add sign 
        </v-btn>
        <v-row>
        </v-row>
    </v-container>    
</template>

<script>
 export default {
    methods:{
     goto_addsign(){
<<<<<<< HEAD
      this.$router.push(`/addsign?library_id=${route.params.id}`);
=======
      this.$router.push('/addsign?library_id=${router.params.id}');
>>>>>>> 3a4622f... Added a library id to /addsign route from the code River pushed to main
    }, 
  },
 }
</script>
