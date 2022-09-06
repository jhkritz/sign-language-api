<!-- References:https://www.digitalocean.com/community/tutorials/how-to-handle-file-uploads-in-vue-2 -->
<template>
    <div>
        <v-form v-model="valid">
            <v-container>
                <v-row id='row'>
                    <v-col>
                        <v-container id='container'>
                            <v-file-input label='Upload a hand sign' v-model='image' />
                                <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required></v-text-field>
                                <v-btn dark color="orange darken-4" depressed @click="postSign">
                                    Submit
                                </v-btn>
                        </v-container>
                        <v-container id='container'>
                            <v-container-title>Take picture to upload</v-container-title>
                                <video id='webcamVideo' width='100%' height='400' autoplay />
                                    <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required>
                                </v-text-field>
                                    <v-btn dark color="orange darken-4">
                                        Submit
                                    </v-btn>
                                    
            </v-container>
                    </v-col>
                </v-row>
            </v-container>
        </v-form>
    </div>
</template>

<style>
    #row {
        align-content: start;
        justify-content: start;
    }
</style>

<script>
    import {
        sharedState
    } from '../SharedState';
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
        created() {
            this.initCamera();
        },
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
                        console.log(JSON.stringify(response.data))
                    })
                    .catch(function(error) {
                        console.log(error);
                        alert('Failed to upload image')
                    })
                        this.signname=" " 
                        this.image = " ";
            },
            async initCamera() {
                this.cameraStream = await window.navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                const videoElement = document.querySelector('video#webcamVideo');
                videoElement.srcObject = this.cameraStream;
                this.imgCapture = new ImageCapture(this.cameraStream.getVideoTracks()[0]);
                sharedState.setCameraStream(this.cameraStream);
            },   
        },

    }
</script>


