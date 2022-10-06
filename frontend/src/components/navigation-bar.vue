<template>
    <v-app-bar app color=#3AAFA9>
        <v-btn icon color="white" id='homeButton' to='/dashboard'>
            <v-icon>mdi-home</v-icon>
        </v-btn>
        <v-app-bar-title id='toolbarTitle' class="white--text">
            {{libraryname}}
        </v-app-bar-title>
        <v-tabs centered class="ml-n9">
            <v-tab v-for="link in links" :key="link.text" :to='link.route'>
                {{link.text}}
            </v-tab>
        </v-tabs>
        <v-menu>
            <template v-slot:activator="{ on, attrs }">
                <v-btn color="white" icon v-bind="attrs" v-on=on>
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

                    <v-list-item @click="navigateToPermissions">
                        <v-list-item-title>
                            Manage permissions
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
        baseUrl
    } from '../BaseRequestUrl';
    export default {
        data: () => ({
            links: [{
                    text: 'Explore library',
                    route: `/library/explore?library_id=${localStorage.getItem('library_id')}`
                },
                {
                    text: 'Interpet my hand signs',
                    route: `/library/test?library_id=${localStorage.getItem('library_id')}`
                },
            ],
            libraryname: localStorage.getItem('library_id')
        }),
        methods: {
            navigateToAPI() {
                this.$router.push(`/library/api?library_id=${localStorage.getItem('library_id')}`);
            },
            navigateToPermissions() {
                this.$router.push(`/library/permissions?library_id=${localStorage.getItem('library_id')}`);
            },
            async deleteLibrary() {
                var axios = require('axios');
                const url = new URL(baseUrl + '/library/deletelibrary');
                url.searchParams.append('library_name', localStorage.getItem('library_id'));
                var config = {
                    method: 'delete',
                    url: url,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    },
                };
                try {
                    const response = await axios(config);
                    console.log(response);
                    // Navigate home after deleting library.
                    this.$router.push('/dashboard');
                } catch (err) {
                    console.error(err);
                }
            },
        }
    }
</script>
