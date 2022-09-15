<template>
    <v-container>
        <h1>
            Your current API Key is :
        </h1> 
        <br/>
        <p class="font-weight-regular">
            {{APIkey}}
        </p>
        <h3>
            Click here to update your API key (note that this will make your previous API key void).
        </h3>
        <br/>
        <v-btn
            color=#17252A
            class="mr-4 white--text"
            @click="UpdateApi"
        >
            Update API_key
        </v-btn>
        <br/>
        <br/>
        <br/>
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
        },
        UpdateApi(){
            this.$router.push("/api/resetapikey")
        }
    },
}
</script>
