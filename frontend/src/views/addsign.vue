<template>
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-form v-model="valid">
                <v-container id='sheet'>
                    <v-sheet id='sheet' min-height="70vh" rounded="lg">
                        <v-row id='row'>
                            <v-row>
                                <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required></v-text-field>
                            </v-row>
                            <v-col>
                                <v-container id='container'>
                                    <v-file-input label='Upload a hand sign' v-model='image' />
                                    <v-btn dark color=#17252A depressed @click="postSign">
                                        Submit single image
                                    </v-btn>
                                </v-container>
                            </v-col>
                            <v-col>
                                <v-container id='container'>
                                    <v-file-input label='Upload a zip file with many photos of the same sign' v-model='zip_file' />
                                    <v-btn dark color=#17252A depressed @click="postSigns">
                                        Submit zip file
                                    </v-btn>
                                </v-container>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-card id='card' class='justify-center align-center'>
                                <v-card-title class='justify-center align-center'>
                                    Camera
                                </v-card-title>
                                <video id='webcamVideo' width='100%' height='400' autoplay />
                                <v-card-actions class='justify-center align-center'>
                                    <v-btn dark color=#17252A @click.stop='postSignVideo'>
                                        Submit video
                                    </v-btn>
                                    <v-btn dark color=#17252A @click.stop='toggleRecording'>
                                        Toggle recording
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-row>
                    </v-sheet>
                </v-container>
            </v-form>
        </v-main>
    </div>
</template>

<style>
    #row {
        align-content: start;
        justify-content: start;
    }

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
            signrules: [
                v => !!v || 'Sign name is required'
            ],
            image: null,
            zip_file: null,
            videoRecorder: null,
            videoRecorded: [],
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
                    data: data,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert('Success');
                    }
                } catch (err) {
                    console.error(err);
                    alert('Failed to upload image.');
                }
            },
            async postSigns() {
                const data = new FormData();
                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                data.append('zip_file', this.zip_file);
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/uploadsigns',
                    data: data,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert(res.data.message);
                    }
                } catch (err) {
                    console.error(err);
                    alert('Failed to upload image')
                }
            },
            async postSignVideo() {
                const data = new FormData();
                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                console.log(this.videoRecorded);
                data.append('video', new Blob(this.videoRecorded.map(e => e.data), {
                    type: 'video/webm'
                }));
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/upload_sign_video',
                    data: data,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        alert(res.data.message);
                    }
                } catch (err) {
                    console.error(err);
                    alert('Failed to upload video');
                }
            },
            async initCamera() {
                this.cameraStream = await window.navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                const videoElement = document.querySelector('video#webcamVideo');
                videoElement.srcObject = this.cameraStream;
                this.videoRecorder = new MediaRecorder(this.cameraStream, {
                    mimeType: 'video/webm'
                });
                this.videoRecorder.addEventListener(
                    'dataavailable', (data) => this.videoRecorded.push(data)
                );
                sharedState.setCameraStream(this.cameraStream);
            },
            async toggleRecording() {
                if (this.videoRecorder.state === 'inactive') {
                    this.videoRecorder.start(100);
                } else if (this.videoRecorder.state === 'paused') {
                    this.videoRecorder.resume();
                } else {
                    this.videoRecorder.pause();
                }
                console.log(this.videoRecorder.state);
            },
        },
    }
</script>
