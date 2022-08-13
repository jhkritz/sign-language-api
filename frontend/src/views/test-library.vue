<template id="test_library">
    <v-container>
        <v-btn @click.stop='toggleStream'>
            Click here to toggle streaming
        </v-btn>
        <video id='webcamVideo' width='300' height='200' autoplay />
        <img id='processedImage' width='300' height='200' />
    </v-container>
</template>

<script charset="utf-8">
    const {
        io
    } = require("socket.io-client");
    export default {
        props: ['lib_name'],
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
                this.socket.emit('image_request', img, this.lib_name);
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
