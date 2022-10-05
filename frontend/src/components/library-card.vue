<template>
    <v-card class="mx-auto" elevation=6 height="10em" width="23em">
        <v-card-text>
            <p class="text-h4 text--primary">
                {{libraryname}}
            </p>
            <div class="text--primary">
                {{librarydesc}}
            </div>
        </v-card-text>
        <v-card-actions>
            <v-btn text color="deep-purple accent-4" @click.stop='navigateToLibraryPage'>
                Explore
            </v-btn>
            <v-btn text color="deep-purple accent-4" @click.stop='navigateToAPI'>
                Use API
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import {
    sharedState
} from '../SharedState';
export default {
    props: {
        libraryname: {
            required: true,
            type: String
        },
        librarydesc: {
            required: true,
            type: String
        }
    },
    methods: {
        navigateToLibraryPage() {
            sharedState.setLibraryID(this.libraryname);
            this.$router.push(`/library/explore?library_id=${this.libraryname}`);
        },
        navigateToAPI() {
            sharedState.setLibraryID(this.libraryname);
            this.$router.push(`/library/api?library_id=${this.libraryname}`);
        }
    }
};
</script>
