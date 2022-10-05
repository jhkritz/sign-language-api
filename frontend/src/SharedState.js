export const sharedState = {

	API_key: null,
	cameraStream: null,

	setAPIkey(newAPIkey) {
		this.API_key = newAPIkey;
	},

	setCameraStream(newCamStream) {
		this.cameraStream = newCamStream;
	},

	stopCamera() {
		if (this.cameraStream != null) {
			this.cameraStream.getVideoTracks()[0].stop();
			this.cameraStream = null;
		}
	}
};
