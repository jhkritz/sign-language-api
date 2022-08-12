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
                <v-sheet id='sheet' min-height="70vh" rounded="lg">
                    <v-row>
                        <v-col cols='2' />
                        <v-col id='col' cols="3">
                            <h3>Signs</h3>
                        </v-col>
                        <v-col cols='1' />
                        <v-col id='col' cols="3">
                            <v-autocomplete label='Search' />
                        </v-col>
                        <v-col cols='1'>
                            <v-btn icon @click.stop='() => navigate("library/addsign")'>
                                <v-icon>mdi-plus</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row id='row'>
                        <v-col cols="12" sm="8">
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
                        </v-col>
                    </v-row>
                </v-sheet>
            </v-container>
        </v-main>
    </v-app>
</template>
<style>
    #col {
        justify-content: center;
        align-content: center;
    }

    #searchBar {
        justify-content: center;
        align-content: center;
        padding: 8;
        box-sizing: border-box;
    }

    #sheet {
        width: 100%;
    }

    #toolRow {
        padding: 8;
        box-sizing: border-box;
    }

    #headingCol {
        align-content: center;
        justify-content: center;
    }

    #row {
        width: 100%;
        align-content: center;
        justify-content: center;
    }

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
