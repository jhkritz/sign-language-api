<template>
    <v-app>
        <v-main>
            <navBar app v-if="shouldDisplayNavbar()" />
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
        methods: {
            shouldDisplayNavbar() {
                const path = this.$router.currentRoute.path;
                return path !== '/' && path !== '/register';
            }
        },
    };
</script>
