<template>
    <v-app id="inspire">
        <v-app-bar app color="white" flat>
            <v-btn icon id='homeButton' @click.stop='()=> navigate("/")'>
                <v-icon>mdi-home</v-icon>
            </v-btn>
            <v-tabs centered class="ml-n9" color="grey darken-1">
                <v-tab v-for="link in links" :key="link.text" @click.stop='() => navigate(link.route)'>
                    {{link.text}}
                </v-tab>
            </v-tabs>
            <v-btn icon>
                <v-icon>mdi-menu</v-icon>
            </v-btn>
        </v-app-bar>
        <v-main class="grey lighten-3">
            <v-container>
                <v-row class="justify-center align-center">
                    <v-col cols="12" sm="8">
                        <v-sheet min-height="70vh" rounded="lg" class="pa-8">
                            <v-simple-table>
                                <thead>
                                    <th id='checkbox' />
                                    <th id='tableText'>
                                        Sign
                                    </th>
                                    <th id='tableText'>
                                        Status
                                    </th>
                                    <th id='buttons' />
                                </thead>
                                <tbody>
                                    <tr v-for="sign in signs" :key="sign.id">
                                        <td id='checkbox'>
                                            <v-checkbox />
                                        </td>
                                        <td id='tableText'>{{sign.meaning}}</td>
                                        <td id='tableText'>{{sign.status}}</td>
                                        <td id='buttons'>
                                            <v-btn icon>
                                                <v-icon>mdi-pencil</v-icon>
                                            </v-btn>
                                            <v-btn icon>
                                                <v-icon>mdi-delete</v-icon>
                                            </v-btn>
                                        </td>
                                    </tr>
                                </tbody>
                            </v-simple-table>
                        </v-sheet>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>
<style>
    #homeButton {
        margin: 1%;
        margin-left: 1px;
        padding: 1%;
        box-sizing: border-box
    }

    #buttons {
        width: 15%
    }

    /* TODO: If anyone knows how to get the headings to
		align properly with the data text, please help. */
    #checkbox {
        width: 1%
    }

    #tableText {
        text-align: left;
    }
</style>

<script>
    // The template above is based off of the three-column wireframe provided by Vuetify
    const axios = require('axios');
    export default {
        props: {
            library_id: null
        },
        data: () => ({
            links: [{
                    text: 'Explore library',
                    route: ''
                },
                {
                    text: 'Interpet my hand signs',
                    route: 'library/test'
                },
                {
                    text: 'Train',
                    route: ''
                }
            ],
            signs: [{
                id: 0,
                meaning: 'A',
                status: 'Trained'
            }, {
                id: 1,
                meaning: 'B',
                status: 'Trained'
            }],
            signsToDelete: [],
        }),
        beforeMount() {
            this.getSigns();
        },
        methods: {
            async getSigns() {
                try {
                    const url = new URL('http://localhost:5000/library/signs');
                    url.searchParams.append('library_name', this.library_id);
                    const config = {
                        method: 'get',
                        url: url
                    }
                    const res = await axios(config);
                    this.signs = res.data.signs.map(sign => ({
                        ...sign,
                        status: 'Trained'
                    }));
                    console.log(this.signs);
                } catch (err) {
                    console.error(err);
                }
            },
            deleteSigns(signsToDelete) {
                console.log(signsToDelete);
            },
            navigate(route) {
                if (route != '') {
                    this.$router.push(`${route}?library_id=${this.library_id}`);
                } else {
                    console.log('Unimplemented');
                }
            }
        }
    }
</script>
