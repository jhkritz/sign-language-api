<template>
    <v-app-bar app>
        <v-btn icon id='homeButton' to='/'>
            <v-icon>mdi-home</v-icon>
        </v-btn>
        <v-tabs centered class="ml-n9">
            <v-tab v-for="link in links" :key="link.text" :to='link.route'>
                {{link.text}}
            </v-tab>
        </v-tabs>
        <v-menu>
            <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on=on>
                    <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
            </template>

            <v-list>
                <v-list-item-group @click="() => {}">
                    <v-list-item @click='navigateToAPI'>
                        <v-list-item-title>
                            Use API
                        </v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="deleteLibrary">
                        <v-list-item-title>
                            Delete Library
                        </v-list-item-title>
                    </v-list-item>

                </v-list-item-group>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>
<style>
    #homeButton {
        margin: 1%;
        margin-left: 1px;
        padding: 1%;
        box-sizing: border-box
    }
</style>

<script charset="utf-8">
    import {
        sharedState
    } from '../SharedState';
    export default {
        data: () => ({
            links: [{
                    text: 'Explore library',
                    route: `/library/explore?library_id=${sharedState.library_id}`
                },
                {
                    text: 'Interpet my hand signs',
                    route: `/library/test?library_id=${sharedState.library_id}`
                },
            ],
        }),
        methods: {
            navigateToAPI() {
                this.$router.push(`/library/api?library_id=${sharedState.library_id}`);
            },
            async deleteLibrary() {
                var axios = require('axios');
                var data = JSON.stringify({
                    "library_name": sharedState.library_id
                });
                var config = {
                    method: 'delete',
                    url: 'http://localhost:5000/library/deletelibrary',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: data
                };
                try {
                    const response = await axios(config);
                    console.log(response.data);
                    // Navigate home after deleting library.
                    this.$router.push('/');
                } catch (err) {
                    console.error(err);
                }
            },
        }
    }
</script>
