<template>
    <v-card class="mx-auto" elevation=6 height="10em" width="23em">
        <v-card-title>
                <span v-text="libraryname" class="text-h4 text--primary" />
        </v-card-title>
        <v-card-text>
            <div class="text--primary">
                {{librarydesc}}
            </div>
        </v-card-text>
        <v-card-actions>
            <v-btn text color="#17252A" @click.stop='navigateToLibraryPage'>
                Explore
            </v-btn>
            <v-btn text color="#17252A" @click.stop='navigateToAPI'>
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
                localStorage.setItem('library_id', this.libraryname);
                this.$router.push(`/library/explore?library_id=${this.libraryname}`);
                this.$emit('library-btn:clicked');
            },
            navigateToAPI() {
                localStorage.setItem('library_id', this.libraryname);
                this.$router.push(`/ViewApi`);
            }
        }
    };
</script>
