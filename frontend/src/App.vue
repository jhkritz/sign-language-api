<template>
  <v-app>
		<toolbar /> 
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import toolbar from './components/toolbar';
export default {
  name: "App",
  data: () => ({
  }),
	components: { 
		toolbar
	},
};
</script>
