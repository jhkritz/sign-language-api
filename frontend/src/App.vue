<template>
  <v-app>
		<Toolbar /> 
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Toolbar from './components/Toolbar';
export default {
  name: "App",
  data: () => ({
  }),
	components: { 
		Toolbar
	},
};
</script>
