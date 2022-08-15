<template>
    <!-- color="teal accent-4" dense dark-->
    <!--            <v-toolbar-title>{{ library_id }}</v-toolbar-title>-->
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-container id='sheet'>
                <v-sheet id='sheet' min-height="70vh" rounded="lg">
                    <v-data-table :headers="headers" :items="signs" class="elevation-1">
                        <template v-slot:top>
                            <v-toolbar flat>
                                <v-toolbar-title>My Signs</v-toolbar-title>
                                <v-divider class="mx-4" inset vertical></v-divider>
                                <v-spacer></v-spacer>
                                <v-btn color="teal accent -4" class="mb-2" v-bind="attrs" v-on="on" @click="goto_addsign">
                                    Add Sign
                                </v-btn>
                                <v-dialog v-model="dialogDelete" max-width="500px">
                                    <v-card>
                                        <v-card-title class="text-h5">Are you sure you want to delete this sign?</v-card-title>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                                            <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                                            <v-spacer></v-spacer>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </v-toolbar>
                        </template>
                        <template v-slot:item.actions="{ item }">
                            <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
                            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
                        </template>
                        <template v-slot:no-data>
                            <v-btn color="primary" @click="initialize"> Reset </v-btn>
                        </template>
                    </v-data-table>
                </v-sheet>
            </v-container>
        </v-main>
    </div>
</template>
<style>
    #sheet {
        width: 100%;
        padding: 2.5%;
        box-sizing: border-box;
    }

    #mainContainer {
        height: 100%;
        box-sizing: border-box;
    }
</style>

<script>
    const axios = require('axios');
    export default {
        components: {},
        props: {
            library_id: null
        },
        data: () => ({
            dialog: false,
            dialogDelete: false,
            headers: [{
                    text: "Sign",
                    align: "start",
                    sortable: false,
                    value: "name",
                },
                {
                    text: "Status",
                    value: "status"
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
            console.log(this.$router.currentRoute);
            this.getSigns();
            //this.initialize();
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
                        name: sign.meaning,
                        status: 'Trained'
                    }));
                    console.log(this.signs);
                } catch (err) {
                    console.error(err);
                }
            },
            goto_addsign() {
                this.$router.push(`/library/addsign?library_id=${this.library_id}`);
            },
            initialize() {
                this.signs = [{
                    name: "A",
                    status: "Trained",
                }, {
                    name: "B",
                    status: "Trained",
                }, {
                    name: "C",
                    status: "Not trained",
                }, ];
            },

            editItem(item) {
                this.editedIndex = this.signs.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.dialog = true;
            },

            deleteItem(item) {
                this.editedIndex = this.signs.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.dialogDelete = true;
            },

            deleteItemConfirm() {
                this.signs.splice(this.editedIndex, 1);
                this.closeDelete();
            },

            close() {
                this.dialog = false;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },

            closeDelete() {
                this.dialogDelete = false;
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
