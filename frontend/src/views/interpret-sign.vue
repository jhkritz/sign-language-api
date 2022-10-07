<template id="test_library">
    <v-main class='grey lighten-3' id='mainContainer'>
        <v-container id='signInterpretationContainer'>
            <v-row id='row'>
                <v-col lg='4' md='6'>
                    <v-card id='signMediaCard' class='justify-center align-center'>
                        <v-card-title class='justify-center align-center'>
                            Camera
                        </v-card-title>
                        <video id='interpretationVideo' autoplay class='mediaElement' />
                        <v-card-actions class='justify-center align-center'>
                            <v-btn dark color=#17252A @click.stop='processSnapshot'>
                                Process a snapshot
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col lg='4' md='6'>
                    <v-card id='signMediaCard' class='justify-center align-center'>
                        <v-card-title class='justify-center align-center'>
                            Processed Image
                        </v-card-title>
                        <v-img :src="processedImageSrc" class='mediaElement' id='processedImage' contain :aspect-ratio='16/9' />
                        <v-card-subtitle class='justify-center align-center'>
                            Sign meaning: {{result.classification}}<br />
                            Confidence: {{result.quality_of_match}}
                        </v-card-subtitle>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>
<style scoped>
    #signInterpretationContainer {
        width: 100%;
        padding: 2.5%;
        box-sizing: border-box;
        min-height: 70vh;
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
            min-height: 50vh;
            border-radius: 10px;
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

<script charset="utf-8">
    const axios = require('axios');
    import {
        sharedState
    } from '../SharedState';
    import {
        baseUrl
    } from '../BaseRequestUrl';
    export default {
        props: ['library_id'],
        data: () => ({
            imgCapture: null,
            cameraStream: null,
            result: {
                classification: 'Unknown',
                quality_of_match: '0%',
            },
            processedImageSrc: null,
        }),
        async created() {
            this.initCamera();
            const config = {
                method: 'get',
                url: baseUrl + '/library/image?image_name=default.jpg&library_name=',
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token')
                }
            };
            try {
                const res = await axios(config);
                this.processedImageSrc = res.data;
                console.log(res);
            } catch (err) {
                console.log(err);
            }
        },
        methods: {
            async processSnapshot() {
                const img = await this.imgCapture.takePhoto();
                const data = new FormData();
                data.append('library_name', this.library_id);
                data.append('image', img);
                const config = {
                    method: 'post',
                    url: baseUrl + '/library/classifyimage',
                    data: data,
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token')
                    }
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
                const videoElement = document.querySelector('video#interpretationVideo');
                videoElement.srcObject = this.cameraStream;
                this.imgCapture = new ImageCapture(this.cameraStream.getVideoTracks()[0]);
                sharedState.setCameraStream(this.cameraStream);
            },
        }
    }
</script>
