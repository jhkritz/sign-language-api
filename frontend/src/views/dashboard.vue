<template>
    <div>
        <div class="header">
            <div class="center">

                <p class="maintitle">Sign Language API</p>
                <v-toolbar flat floating rounded>
                    <v-text-field v-model="libraries.name" hide-details label="Search for a library..." prepend-icon="mdi-magnify" single-line @input="filterLibraries">
                    </v-text-field>
                </v-toolbar>
            </div>
        </div>



        <div class="addLibraryButton">
            <v-row justify="center">
                <v-dialog v-model="dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn class="mx-2" fab dark color="#17252A" v-bind="attrs" v-on="on">
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
                                        <v-text-field v-model="myName" label="Library name" required></v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field v-model="myDesc" label="Description" required></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="#17252A" text @click="dialog = false">
                                Close
                            </v-btn>
                            <v-btn color="#17252A" text @click="addNewLibrary">
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-row>
        </div>
        <div class='libraries'>
            <libraryCardVue v-for="library in filteredList" :key="library.name" :libraryname="library.name" :librarydesc="library.description" />
        </div>
    </div>
</template>
<script>
    import libraryCardVue from '../components/library-card.vue';
    import {
        baseUrl
    } from '../BaseRequestUrl.js';

    const axios = require('axios');
    export default {
        data: () => ({
            dialog: false,
            myName: '',
            myDesc: '',
            libraries: [],
            filteredList: [],
        }),
        components: {
            libraryCardVue
        },
        methods: {
            async addAllLibraries() {
                try {
                    const config = {
                        method: 'get',
                        url: baseUrl + '/libraries/getall',
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        }
                    };
                    // Get list of libraries
                    const res = await axios(config);
                    this.libraries = res.data.libraries;
                    this.filteredList = this.libraries.slice();
                } catch (err) {
                    console.error(err);
                }
            },
            async filterLibraries() {
                //let filteredList = [];
                this.filteredList = this.libraries.slice();
                var x = this.libraries.name;
                this.filteredList = this.libraries.filter(item => {
                    return item.name.toLowerCase().includes(x.toLowerCase()) || item.description.toLowerCase().includes(x.toLowerCase())
                });
                console.log(JSON.stringify(this.filteredList));

            },
            async addNewLibrary() {
                try {
                    // add library to database
                    const FormData = require('form-data');
                    const data = new FormData();
                    data.append('library_name', this.myName);
                    data.append('description', this.myDesc);
                    const config = {
                        method: 'post',
                        url: baseUrl + '/library/createlibrary',
                        data: data,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        }
                    };
                    const res = await axios(config);
                    if (res.status !== 200) {
                        alert('Failed to create library.');
                    } else {
                        this.libraries.push({
                            name: this.myName,
                            description: this.myDesc
                        });
                    }
                } catch (err) {
                    alert('Failed to create library.');
                    console.error(err);
                }
                this.filteredList = this.libraries.slice();
                //link buttons to lib id
                this.myName = '';
                this.myDesc = '';
                this.dialog = false;
            },
        },
        beforeMount() {
            this.addAllLibraries()
        }
    }
</script>
<style scoped>
    .header {
        background-repeat: repeat-x;
        min-height: 25vw;
        max-height: 30vw;
        background-image: url('../assets/Tile.svg');
        background-color: #3AA5A9;
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
        padding-top: 2.5%;
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
        max-width: 93%;
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
