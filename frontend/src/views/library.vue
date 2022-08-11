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
		</v-container>
</template>

<script>
 export default {
    methods:{
     goto_addsign(){
      this.$router.push(`/addsign?library_id=${this.$route.params.id}`);
    }, 
  },
 }
</script>
