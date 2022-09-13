<template>
    <h1>
        API Key: 
        <p class="font-weight-regular">
            {{APIkey}}
        </p>
    </h1>
    
</template>

<script>
import { sharedState } from '../SharedState';
export default {
    data: () => ({
        APIkey: sharedState.API_key
}),
}
</script>
