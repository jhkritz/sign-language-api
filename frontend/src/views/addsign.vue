<!-- References:https://www.digitalocean.com/community/tutorials/how-to-handle-file-uploads-in-vue-2 -->
<template>
    <v-form v-model="valid">
        <v-container>
            <!-- UPLOAD SIGN -->
            <h1>Add sign</h1>
            <v-container id='container'>
                <v-file-input label='Upload a hand sign' v-model='image' />
            </v-container>
            <div class="dropbox">
                <input type="file" single required>
            </div>
            <!-- SIGN NAME -->
            <v-col cols="12" sm="6" md="3">
                <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required></v-text-field>
            </v-col>
            <v-btn depressed @click="postSign">
                Submit
            </v-btn>
        </v-container>
    </v-form>
</template>

<script>
    export default {
        props: {
            library_id: null
        },
        data: () => ({
            valid: false,
            signname: '',
            signrules: [
                v => !!v || 'Sign name is required'
            ],
            image: null
        }),
        methods: {
            async postSign() {
                // Accessing search parameters
                // ----------------------------
                console.log(this.library_id);
                // ----------------------------
                var axios = require('axios');
                var FormData = require('form-data');

                var data = new FormData();
                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                data.append('image_file', this.image);

                var config = {
                    method: 'post',
                    url: 'http://localhost:5000/library/uploadsign',
                    data: data
                };

                axios(config)
                    .then(function(response) {
                        console.log(JSON.stringify(response.data));
                    })
                    .catch(function(error) {
                        console.log(error);
                    });
            }
        },

    }
</script>

<!-- SASS styling -->
<style lang="scss">
    .dropbox {
        outline: 2px dashed grey;
        /* the dash box */
        outline-offset: -10px;
        background: lightcyan;
        color: dimgray;
        padding: 10px 10px;
        min-height: 200px;
        /* minimum height */
        position: relative;
        cursor: pointer;
    }

    .input-file {
        opacity: 0;
        /* invisible but it's there! */
        width: 100%;
        height: 200px;
        position: absolute;
        cursor: pointer;
    }

    .dropbox:hover {
        background: lightblue;
        /* when mouse over to the drop zone, change color */
    }

    .dropbox p {
        font-size: 1.2em;
        text-align: center;
        padding: 50px 0;
    }

    #container {
        width: 50%
    }
</style>
