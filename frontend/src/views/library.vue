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
    <v-col
      v-for="n in 9"
      :key="n"
      class="d-flex child-flex"
      cols="4"
    >
      <v-img
        :src="`https://images.agoramedia.com/wte3.0/gcms/baby-sign-launage-722x406.jpg?width=574`"
        
        aspect-ratio="1"
        class="grey lighten-2"
      >
        <template v-slot:placeholder>
          <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
              color="grey lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </v-col>
  </v-row>
    </v-container>    
</template>

<script>
 export default {
    methods:{
     goto_addsign(){
      this.$router.push('/addsign?library_id=${router.params.id}');
    }, 
  },
 }
</script>
