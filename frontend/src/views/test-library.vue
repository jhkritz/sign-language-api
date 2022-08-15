<template id="test_library">
    <div id='mainContainer'>
        <v-main class='grey lighten-3' id='mainContainer'>
            <v-container id='sheet'>
                <v-sheet min-height='70vh' rounded='lg' id='sheet'>
                    <v-row>
                        <v-col>
                            <video id='webcamVideo' width='400' height='300' autoplay />
                        </v-col>
                        <v-col>
                            <img id='processedImage' width='400' height='300' />
                        </v-col>
                    </v-row>
                    <v-container>
                        <v-btn @click.stop='toggleStream'>
                            Toggle streaming
                        </v-btn>
                    </v-container>
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

<script charset="utf-8">
    const {
        io
    } = require("socket.io-client");
    export default {
        props: ['library_id'],
        data: () => ({
            imgCapture: null,
            socket: null,
            cameraStream: null,
            streamInterval: null,
            isStreaming: false,
        }),
        methods: {
            async sendFrame() {
                const img = await this.imgCapture.takePhoto();
                this.socket.emit('image_request', img, this.library_id);
            },
            async receiveFrame(response) {
                const img = document.querySelector('img#processedImage');
                img.src = response.frame;
                console.log(response.result);
            },
            async toggleStream() {
                if (this.isStreaming) {
                    this.stopStream();
                } else {
                    this.initStream();
                }
            },
            async stopStream() {
                this.isStreaming = false;
                window.clearInterval(this.streamInterval);
                this.socket.disconnect();
                this.socket.close();
                this.socket = null;
            },
            async initStream() {
                this.isStreaming = true;
                this.cameraStream = await window.navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                const videoElement = document.querySelector('video#webcamVideo');
                videoElement.srcObject = this.cameraStream;
                this.imgCapture = new ImageCapture(this.cameraStream.getVideoTracks()[0]);
                this.socket = new io("ws://127.0.0.1:5000");
                // Capture and send a new frame every second
                this.streamInterval = window.setInterval(this.sendFrame, 1000);
                // Create an event handler to receive processed frames
                this.socket.on('image_response', this.receiveFrame);
            },
        }
    }
</script>
