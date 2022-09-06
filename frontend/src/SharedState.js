export const sharedState = {
	library_id: null,
	cameraStream: null,
	setLibraryID(newID) {
		// Note: this should only be called from library-card.vue
		// Additional note: at the moment the 'library_id' is actually the library name.
		this.library_id = newID
	},
	setCameraStream(newCamStream) {
		this.cameraStream = newCamStream;
	},
	stopCamera() {
		if (this.cameraStream != null) {
			this.cameraStream.getVideoTracks()[0].stop();
		}
	}
};
