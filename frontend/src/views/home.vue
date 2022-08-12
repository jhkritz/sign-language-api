<style>
    .header {
        background-repeat: repeat-x;
        min-height: 25vw;
        max-height: 30vw;
        background-image: url('../assets/Tile.svg');
        background-color: cadetblue;
        background-size: contain;

    }

    .center {
        text-align: center;
        margin: auto;
        padding: 8%;
    }

    .maintitle {

        padding-bottom: 1%;
        font-size: 4vw;
        color: white;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: lighter;
        backdrop-filter: blur(20px) opacity(0.8);
    }

    .addLibraryButton {
        padding: 2%;
        display: inline-flex;
        position: relative;
        float: right;
    }

    .libraries {
        padding: 2%;
        display: inline-flex;
        align-content: left;
        flex-wrap: wrap;
        flex-direction: row;
        gap: 2vw;
    }

    .libraries>v-card {
        max-height: 10vw;
        max-width: 20vw;
        display: flex;
        justify-content: left;
        justify-items: left;
        align-items: left;

    }
</style>
<template>
    <div>
        <div class="header">
            <div class="center">

                <h1 class="maintitle">Sign Language API</h1>

                <v-toolbar flat floating rounded>
                    <v-text-field hide-details label="Search for a library..." prepend-icon="mdi-magnify" single-line>
                    </v-text-field>
                </v-toolbar>


            </div>
        </div>

        <div class='libraries'>
            <libraryCardVue v-for="library in libraries" :key="library.name" :libraryname="library.name" :librarydesc="library.description" />
        </div>

        <div class="addLibraryButton">
            <v-row justify="center">
                <v-dialog v-model="dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn class="mx-2" fab dark color="indigo" v-bind="attrs" v-on="on">
                            <v-icon dark>
                                mdi-plus
                            </v-icon>
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">Add a new library:</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="12">
                                        <v-text-field v-model="myName" label="Library Name *" required></v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field v-model="myDesc" label="Description *" required></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                            <small>*indicates required field</small>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="indigo" text @click="dialog = false">
                                Close
                            </v-btn>
                            <v-btn color="indigo" text @click="addNewLibrary">
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-row>

        </div>

    </div>
</template>
<script>
    import libraryCardVue from '../components/library-card.vue';
    //import Vue from 'vue';
    const axios = require('axios');
    export default {
        data: () => ({
            dialog: false,
            myName: '',
            myDesc: '',
            libraries: []
        }),
        components: {
            libraryCardVue
        },
        methods: {
            async addAllLibraries() {
                try {
                    const config = {
                        method: 'get',
                        url: 'http://localhost:5000/libraries/getall',
                    };
                    // Get list of libraries
                    const res = await axios(config);
                    console.log(res.data.libraries);
                    this.libraries = res.data.libraries;
                } catch (err) {
                    console.error(err);
                }
            },
            async addNewLibrary() {
                try {
                    //add library to database
                    const FormData = require('form-data');
                    const data = new FormData();
                    data.append('library_name', this.myName);
                    data.append('description', this.myDesc);
                    const config = {
                        method: 'post',
                        url: 'http://localhost:5000/library/createlibrary',
                        data: data
                    };
                    const res = await axios(config);
                    if (res.data.message !== 'Library exists') {
                        this.libraries.push({
                            name: this.myName,
                            description: this.myDesc
                        });
                    }
                } catch (err) {
                    console.error(err);
                }
                //link buttons to lib id
                this.myName = '';
                this.myDesc = '';
                this.dialog = false;
            },
            searchLibraries() {}
        },
        beforeMount() {
            this.addAllLibraries()
        }
    }
</script>
