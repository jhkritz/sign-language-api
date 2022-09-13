<template id="test_library">
    <div id='mainContainer'>
        <v-main class='grey lighten-3' id='mainContainer'>
            <v-container id='sheet'>
                <v-sheet min-height='70vh' rounded='lg' id='sheet'>
                    <v-row id='sheet'>
                        <v-col cols='6'>
                            <v-card id='card' class='justify-center align-center'>
                                <v-card-title class='justify-center align-center'>
                                    Camera
                                </v-card-title>
                                <video id='webcamVideo' width='100%' height='400' autoplay />
                                <v-card-actions class='justify-center align-center'>
                                    <v-btn dark color=#17252A @click.stop='processSnapshot'>
                                        Process a snapshot
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                        <v-col cols='6'>
                            <v-card id='card' class='justify-center align-center'>
                                <v-card-title class='justify-center align-center'>
                                    Processed Image
                                </v-card-title>
                                <v-img id='processedImage' :src='processedImageSrc' width='100%' contain :aspect-ratio='16/9' />
                                <v-card-subtitle class='justify-center align-center'>
                                    Sign meaning: {{result.classification}}<br />
                                    Confidence: {{result.quality_of_match}}
                                </v-card-subtitle>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-sheet>
            </v-container>
        </v-main>
    </div>
</template>
<style>
    #card {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }

    #sheet {
        width: 100%;
        padding: 2.5%;
        box-sizing: border-box;
        justify-content: space-between;
    }

    #mainContainer {
        height: 100%;
        box-sizing: border-box;
    }
</style>

<script charset="utf-8">
    const axios = require('axios');
    import {
        sharedState
    } from '../SharedState';
    export default {
        props: ['library_id'],
        data: () => ({
            imgCapture: null,
            cameraStream: null,
            result: {
                classification: 'Unknown',
                quality_of_match: '0%',
            },
            processedImageSrc: 'http://localhost:5000/library/image?image_name=default.jpg&library_name='
        }),
        created() {
            this.initCamera();
        },
        methods: {
            async processSnapshot() {
                const img = await this.imgCapture.takePhoto();
                const data = new FormData();
                data.append('library_name', this.library_id);
                data.append('image', img);
                const config = {
                    method: 'post',
                    url: 'http://localhost:5000/library/classifyimage',
                    data: data
                };
                try {
                    const res = await axios(config);
                    if (res.status == 200) {
                        this.processedImageSrc = res.data.processedImage;
                        this.result = res.data.result;
                    } else {
                        console.error('classification failed');
                    }
                } catch (err) {
                    console.error(err);
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
        }
    }
</script>
