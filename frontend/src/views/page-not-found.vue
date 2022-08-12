<template>
    <v-container>
        <h1>404: Page not found</h1>
        <v-btn @click.stop='navigateHome'>
            Click here to return to the home page.
        </v-btn>
    </v-container>
</template>
<script>
    export default {
        methods: {
            navigateHome() {
                this.$router.push('/');
            }
        }
    }
</script>
