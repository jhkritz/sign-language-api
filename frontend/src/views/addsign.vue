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
                                Submit single image
                            </v-btn>
                        </v-container>
                    </v-col>
                    <v-col>
                        <v-container id='container'>
                            <v-file-input label='Upload a zip file with many photos of the same sign' v-model='zip_file' />
                            <v-text-field v-model="zip_signname" label="Sign name" :rules="signrules" outlined required />
                            <v-btn dark color="orange darken-4" depressed @click="postSigns">
                                Submit zip file
                            </v-btn>
                        </v-container>
                        <!--
                        <v-container id='container'>
                            <v-container-title>Take picture to upload</v-container-title>
                                <video id='webcamVideo' width='100%' height='400' autoplay />
                                    <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required>
                                </v-text-field>
                                    <v-btn dark color="orange darken-4">
                                        Submit
                                    </v-btn>
                                    
            </v-container>
						-->
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
    import {
        baseUrl
    } from '../BaseRequestUrl';
    const axios = require('axios');
    const FormData = require('form-data');
    export default {
        props: {
            library_id: null
        },
        data: () => ({
            valid: false,
            signname: '',
            zip_signname: '',
            signrules: [
                v => !!v || 'Sign name is required'
            ],
            image: null,
            zip_file: null,
        }),
        created() {
            this.initCamera();
        },
        methods: {

            async postSign() {
                const data = new FormData();

                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                data.append('image_file', this.image);

                const config = {
                    method: 'post',
                    url: baseUrl + '/library/uploadsign',
                    data: data
                };

                axios(config)
                    .then(function(response) {
                        console.log(JSON.stringify(response.data));
                        if (response.status == 200) {
                            alert('Success');
                            this.signname = " "
                            this.image = " ";
                        }
                    })
                    .catch(function(error) {
                        console.log(error);
                        alert('Failed to upload image')
                    })
            },
            async postSigns() {
                const data = new FormData();
                data.append('sign_name', this.zip_signname);
                data.append('lib_name', this.library_id);
                data.append('zip_file', this.zip_file);
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/uploadsigns',
                    data: data
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert('Success');
                        this.signname = " "
                        this.image = " ";
                    }
                } catch (err) {
                    console.error(err);
                    alert('Failed to upload image')
                }
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
