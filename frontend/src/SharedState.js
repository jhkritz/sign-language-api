export const sharedState = {
	library_id: null,
	setLibraryID(newID) {
		// Note: this should only be called from library-card.vue
		// Additional note: at the moment the 'library_id' is actually the library name.
		this.library_id = newID
	},
};
