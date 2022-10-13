<style scoped>
    #signInterpretationContainer {
        width: 100%;
        padding: 2.5%;
        box-sizing: border-box;
        min-height: 70vh;
    }

    #subtitle {
        display: inline-flex;
        text-align: center;
        width: 100%;
        height: 100%;
        flex-direction: column;
    }


    @media (max-width: 998px) {
        .mediaElement {
            border: 25px solid;
            width: 100%;
            box-sizing: border-box;
            min-height: 35vh;
            max-height: 35vh;
            background-color: black;
        }

        #signMediaCard {
            box-sizing: border-box;
            min-height: 45vh;
        }
    }

    @media (min-width: 1100px) {
        .mediaElement {
            border: 25px solid;
            width: 100%;
            box-sizing: border-box;
            min-height: 40vh;
            max-height: 40vh;
            background-color: black;
        }

        #signMediaCard {
            box-sizing: border-box;
            min-height: 55vh;
            border-radius: 10px;
        }
    }
</style>

<template>
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-container id='sheet'>
                <v-row id='row'>
                    <v-col lg='8' md='12'>
                        <v-data-table v-if="showSignTable" :headers="headers" :items="signs" :single-select="singleSelect" item-key="name" show-select @input="selectAll" class="elevation-1">
                            <template v-slot:top>
                                <v-toolbar flat>
                                    <v-toolbar-title>
                                        Library Signs
                                    </v-toolbar-title>
                                    <v-divider class="mx-4" inset vertical>
                                    </v-divider>
                                    <v-spacer></v-spacer>
                                    <v-btn dark color=#17252A class="ma-2">
                                        <v-icon dark small @click="deleteItem(item)"> mdi-delete </v-icon>
                                    </v-btn>
                                    <v-btn dark color=#17252A class="ma-2" @click="goto_addsign">
                                        Add Sign
                                    </v-btn>
                                    <v-dialog v-model="dialogDelete" max-width="500px">
                                        <v-card>
                                            <v-card-title class="text-h5">Are you sure you want to delete this sign?</v-card-title>
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn color=#17252A text @click="closeDelete">Cancel</v-btn>
                                                <v-btn color=#17252A text @click="deleteItemConfirm()">OK</v-btn>
                                                <v-spacer></v-spacer>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
                                </v-toolbar>
                            </template>
                            <template v-slot:item.actions="{ item }">
                                <v-icon small class="mr-2" @click="viewSign(item)"> mdi-eye </v-icon>
                                <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
                                <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
                            </template>
                            <template v-slot:no-data>
                                <v-btn icon>
                                    <v-icon>
                                        mdi-cached
                                    </v-icon>
                                </v-btn>
                            </template>
                        </v-data-table>
                    </v-col>
                    <v-col lg='4' md='6'>
                        <v-card id='signMediaCard' class='justify-center align-center'>
                            <v-card-title class='justify-center align-center'>
                                Selected sign
                            </v-card-title>
                            <v-img class='mediaElement' id='processedImage' v-bind:src=" 'data:image/jpeg;base64,'+imageToView" contain :aspect-ratio='16/9' />
                            <v-card-subtitle id='subtitle'>
                                {{signToView !== null ? `One of ${signToView.number_of_images}associated with '${signToView.name}'` : "Select a sign from the table"}}
                            </v-card-subtitle>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </div>
</template>

<script>
    const axios = require('axios');
    import {
        baseUrl
    } from '../BaseRequestUrl';
    export default {
        components: {},
        props: {
            library_id: null
        },
        data: () => ({
            singleSelect: false,
            selected: [],
            signToView: null,
            imageToView: null,
            signToEdit: null,
            showSignTable: true,
            showEditSignTable: false,
            itemToDelete: null,
            dialogDelete: false,
            headers: [{
                    text: "Sign",
                    align: "start",
                    sortable: false,
                    value: "name",
                },
                {
                    text: "Number of images",
                    value: "number_of_images",
                    sortable: false,
                },
                {
                    text: "Actions",
                    value: "actions",
                    sortable: false
                },
            ],
            signs: [],
            editedIndex: -1,
            editedItem: {
                name: "",
                status: "",
            },
            defaultItem: {
                name: "",
                status: "",
            },
            signsToDelete: [],
        }),

        computed: {
            formTitle() {
                return this.editedIndex === -1 ? "New Item" : "Edit Item";
            },
        },

        watch: {
            dialog(val) {
                val || this.close();
            },
            dialogDelete(val) {
                val || this.closeDelete();
            },
        },

        created() {
            this.getSigns();
        },

        methods: {
            async viewSign(selectedSign) {
                console.log(selectedSign);
                this.signToView = selectedSign;
                try {
                    const url = new URL(baseUrl + '/library/imageb64');
                    url.searchParams.append('library_name', this.library_id);
                    url.searchParams.append('image_name', selectedSign.name);
                    console.log(url);
                    const config = {
                        method: 'get',
                        url: url,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        },
                    }
                    const res = await axios(config);
                    this.imageToView = res.data;
                } catch (err) {
                    console.error(err);
                }
            },
            async getSigns() {
                try {
                    const url = new URL('http://localhost:5000/library/signs');
                    console.log(this.library_id);
                    url.searchParams.append('library_name', this.library_id);
                    const config = {
                        method: 'get',
                        url: url,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        }
                    }
                    const res = await axios(config);
                    this.signs = res.data.signs.map(
                        sign => sign.meaning
                    ).filter(
                        (item, index, self) => self.indexOf(item) === index
                    );
                    const countImages = (meaning) => {
                        var i = 0;
                        res.data.signs.map(sign => {
                            if (sign.meaning === meaning) {
                                i++;
                            }
                        });
                        return i;
                    };
                    this.signs = this.signs.map(meaning => ({
                        name: meaning,
                        number_of_images: countImages(meaning)
                    }));
                } catch (err) {
                    console.error(err);
                }
            },
            selectAll(items) {
                this.selected = [];
                if (items.length > 0) {
                    this.selected = items.map(item => item.name)
                }
                console.dir(this.selected)
            },
            async deleteAll() {
                try {
                    const url = new URL('http://localhost:5000/library/deletesigns');
                    const data = {
                        library_name: this.library_id,
                        signs: this.selected

                    };
                    const config = {
                        method: 'get',
                        url: url,
                        data: data,
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem('access_token')
                        }
                    }
                    const res = await axios(config);
                    console.log(res)
                } catch (err) {
                    console.error(err);
                }

            },

            goto_addsign() {
                this.$router.push(`/library/addsign?library_id=${this.library_id}`);
            },

            editItem(item) {
                this.signToEdit = item.name;
                this.editedIndex = this.signs.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.swapTable();
            },

            swapTable() {
                if (this.showSignTable) {
                    this.showEditSignTable = true;
                    this.showSignTable = false;
                } else {
                    this.showEditSignTable = false;
                    this.showSignTable = true;
                }
            },

            deleteItem(item) {
                this.editedIndex = this.signs.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.itemToDelete = item.name;
                this.dialogDelete = true;
            },

            async deleteItemConfirm() {
                const url = new URL(baseUrl + '/library/deletesign');
                url.searchParams.append('library_name', localStorage.getItem('library_id'));
                url.searchParams.append('sign_name', this.itemToDelete);
                const config = {
                    method: 'delete',
                    url: url,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    },
                };
                try {
                    await axios(config);
                } catch (err) {
                    this.closeDelete();
                    alert('Failed to delete sign.');
                    return;
                }
                this.signs.splice(this.editedIndex, 1);
                this.closeDelete();
            },

            closeDelete() {
                this.dialogDelete = false;
                this.itemToDelete = null;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },

            save() {
                if (this.editedIndex > -1) {
                    Object.assign(this.signs[this.editedIndex], this.editedItem);
                } else {
                    this.signs.push(this.editedItem);
                }
                this.close();
            },

        },
    };
</script>
