<template>
    <v-container>
        <h1>
            API Key:
        </h1> 
        <p class="font-weight-regular">
            {{APIkey}}
        </p>
        <v-btn
            color=#17252A
            class="mr-4 white--text"
            @click="goToDashboard"
        >
            Done
        </v-btn>
    </v-container>
</template>

<script>
import { sharedState } from '../SharedState';
export default {
    data: () => ({
        APIkey: sharedState.API_key
    }),
    methods: {
        goToDashboard(){
            this.$router.push("/dashboard");
        }
    },
}
</script>
