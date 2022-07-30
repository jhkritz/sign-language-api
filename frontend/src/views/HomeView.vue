<template>
  <v-app fluid class="head">
    <div>
      <v-row justify="center">
        <v-col cols="12" sm="8">
          <v-container>
            <v-content class="content">
              <h1 class="black--text">Find</h1>
            </v-content>

            <v-content class="cont1">
              <v-btn
                rounded
                color="black"
                dark
                @click="goToLogin()"
                class="mr-10 mt-15 mb-10"
              >
                LOGIN
              </v-btn>
            </v-content>

            <v-content class="cont2">
              <v-btn
                rounded
                color="black"
                dark
                @click="goToSignUp()"
                class="mt-15"
              >
                SIGNUP
              </v-btn>
            </v-content>
          </v-container>
        </v-col>
      </v-row>
    </div>
  </v-app>
</template>

<script>
export default {
  name: "Home",

  components: {},

  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    goToSignUp() {
      this.$router.push("/register");
    },
  },
};
</script>
 
<style scoped>
.head {
  width: 100vw;
  height: 100vh;
  background-image: url(./../assets/friends.gif);
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
}

.content {
  position: absolute;
  top: 35%;
  left: 25%;
  transform: translateY(-50%);
  z-index: 2;
}

.cont1 {
  position: absolute;
  top: 56%;
  left: 25%;
  transform: translateY(-50%);
  z-index: 2;
}

.cont2 {
  position: absolute;
  top: 54%;
  left: 68%;
  transform: translateY(-50%);
  z-index: 2;
}
</style>