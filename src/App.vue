<template>
    <v-app>
        <v-main>
            <navBar app v-if="this.$router.currentRoute.path !== '/'" />
            <router-view />
        </v-main>
    </v-app>
</template>

<script>
    import navBar from './components/navigation-bar';
    export default {
        name: "App",
        data: () => ({}),
        components: {
            navBar
        },
    };
</script>
