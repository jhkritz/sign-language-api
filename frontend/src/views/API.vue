<template>
    <h1>
        API Key: {{APIkey}}
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
