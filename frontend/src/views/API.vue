<template>
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-container id='sheet'>
                <v-sheet id='sheet' min-height="70vh" rounded="lg">
                    <h1>
                        API Key:
                    </h1>
                    <p class="font-weight-regular">
                        {{APIkey}}
                    </p>
                    <v-btn color=#17252A class="mr-4 white--text" @click="goToDashboard">
                        Done
                    </v-btn>
                </v-sheet>
            </v-container>
        </v-main>
    </div>
</template>

<style scoped>
    #sheet {
        width: 100%;
        padding: 2.5%;
        box-sizing: border-box;
    }

    #mainContainer {
        height: 100%;
        box-sizing: border-box;
    }
</style>

<script>
    import {
        sharedState
    } from '../SharedState';
    export default {
        data: () => ({
            APIkey: sharedState.API_key
        }),
        methods: {
            goToDashboard() {
                this.$router.push("/dashboard");
            }
        },
    }
</script>
