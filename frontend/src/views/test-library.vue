<template id="test_library">
    <v-container>
        <v-btn @click.stop='initStream'>
            Click here to start streaming
        </v-btn>
        <video id='webcamVideo' width='300' height='200' autoplay />
    </v-container>
</template>

<script charset="utf-8">
    const {
        io
    } = require("socket.io-client");
    export default {
        data: () => ({
            imgCapture: null,
            socket: null,
            cameraStream: null,
        }),
        methods: {
            async sendFrame() {
                const img = await this.imgCapture.takePhoto();
                console.log(img);
                this.socket.emit('image_request', img);
            },
            async receiveFrame(frame) {
                console.log('frame received');
                console.log(frame);
            },
            async initStream() {
                console.log('init');
                this.cameraStream = await window.navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                const videoElement = document.querySelector('video#webcamVideo');
                videoElement.srcObject = this.cameraStream;
                this.imgCapture = new ImageCapture(this.cameraStream.getVideoTracks()[0]);
                this.socket = new io("ws://127.0.0.1:5000");
                // Capture and send a new frame every 30 milliseconds
                window.setInterval(this.sendFrame, 30);
                // Create an event handler to receive processed frames
                this.socket.on('image_response', this.receiveFrame);
            },
        }
    }
</script>
