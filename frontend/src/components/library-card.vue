<template>
    <v-card class="mx-auto" elevation=6>
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
            <v-btn text color="deep-purple accent-4">
                Use API
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
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
                this.$router.push(`/library?id=${this.libraryname}`);
            }
        }
    };
</script>
