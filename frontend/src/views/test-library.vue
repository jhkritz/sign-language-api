<template id="test_library">
<v-container>
<v-btn @click.stop='streamVideo'/>
<video id='webcamVideo' width='300' height='200' autoplay>
</video>
</v-container>
</template>

<script charset="utf-8">
const {
	io
} = require("socket.io-client");
export default {
	data: () => ({
	}),
	methods: {
		async streamVideo() {
			const stream = await window.navigator.mediaDevices.getUserMedia({video: true, audio:false});
			const videoElement = document.querySelector('video#webcamVideo');
			videoElement.srcObject = stream;
			const socket = new io("ws://127.0.0.1:5000");
			socket.on('after_connect', () => console.log('after_connect'));
			socket.on('connect', () => {console.log('This is works'); socket.emit('log')});
		} 
	}
}
</script>
