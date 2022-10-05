<template>
    <div id='mainContainer'>
        <v-main class="grey lighten-3" id='mainContainer'>
            <v-form v-model="valid">
                <v-container id='sheet'>
                    <v-sheet id='sheet' rounded="lg" class='justify-center align-center'>

                        <v-row id="row">
                            <v-tabs centered v-model="selectedOption" @change="handleOptionChange">
                                <v-tab v-for="option in options" :key="option">
                                    {{ option }}
                                </v-tab>
                            </v-tabs>
                        </v-row>

                        <v-row id="row">
                            <v-col cols=6>
                                <v-text-field v-model="signname" label="Sign name" :rules="signrules" outlined required />
                            </v-col>
                        </v-row>

                        <v-row id="row" v-if="selectedOption === 1">
                            <v-col cols=6>
                                <v-file-input label='Upload an image' v-model='file' />
                            </v-col>
                        </v-row>

                        <v-row id="row" v-if="selectedOption === 2">
                            <v-col cols=6>
                                <v-file-input label='Upload a zip file containing images' v-model='file' />
                            </v-col>
                        </v-row>

                        <v-row id="row" v-if="selectedOption === 0">
                            <v-col cols=6>
                                <video id='webcamVideo' autoplay />
                            </v-col>
                        </v-row>

                        <v-row id="row" v-if="selectedOption === 0">
                            <v-col cols=6>
                                <v-btn dark color=#17252A @click.stop='toggleRecording'>
                                    {{ recording ? "Stop recording" : "Start recording" }}
                                </v-btn>
                            </v-col>
                        </v-row>

                        <v-row id="row">
                            <v-col cols=6 id="row">
                                <v-btn dark color=#17252A depressed @click="submitInput">
                                    Submit
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-sheet>
                </v-container>
            </v-form>
        </v-main>
    </div>
</template>

<style>
    #row {
        align-content: center;
        justify-content: center;
        box-sizing: border-box;
        display: flex;
    }

    #sheet {
        width: 100%;
        padding: 2.5%;
        min-height: 80vh;
        box-sizing: border-box;
        text-align: center;
    }

    #mainContainer {
        height: 100%;
        box-sizing: border-box;
    }

    #webcamVideo {
        border: 3px solid;
        width: 100%;
        display: none;
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
            options: ['Video', 'Single image', 'Zip file'],
            selectedOption: 0,
            recording: false,
        }),
        created() {
            this.initCamera();
        },
        methods: {
            handleOptionChange() {
                if (this.selectedOption === 0) {
                    this.initCamera();
                } else {
                    this.cameraStream.getVideoTracks()[0].stop();
                    this.cameraStream = null;
                }
            },
            async submitInput() {
                const data = new FormData();
                data.append('sign_name', this.signname);
                data.append('lib_name', this.library_id);
                var url = '';
                switch (this.selectedOption) {
                    case 0:
                        url = baseUrl + '/library/upload_sign_video';
                        data.append('video', new Blob(this.videoRecorded.map(e => e.data), {
                            type: 'video/webm'
                        }));
                        break;
                    case 1:
                        url = baseUrl + '/library/uploadsign';
                        data.append('image_file', this.file);
                        break;
                    case 2:
                        url = baseUrl + '/library/uploadsigns';
                        data.append('zip_file', this.file);
                        break;
                    default:
                        console.log('Error: default case reached.');
                        break;
                }
                const config = {
                    method: 'post',
                    url: url,
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
                await videoElement.load();
                videoElement.style.display = "block";
                sharedState.setCameraStream(this.cameraStream);
            },
            async toggleRecording() {
                const videoElement = document.querySelector('video#webcamVideo');
                if (this.recording) {
                    this.videoRecorder.pause();
                    this.recording = false;
                    videoElement.style.border = "3px solid";
                } else if (this.videoRecorder != null) {
                    this.videoRecorder.resume();
                    this.recording = true;
                    videoElement.style.border = "3px solid #ff0000";
                } else {
                    this.videoRecorder = new MediaRecorder(this.cameraStream, {
                        mimeType: 'video/webm'
                    });
                    this.videoRecorder.addEventListener(
                        'dataavailable', (data) => this.videoRecorded.push(data)
                    );
                    this.videoRecorder.start(100);
                    this.recording = true;
                    videoElement.style.border = "3px solid #ff0000";
                }
            },
        },
    }
</script>
