<template>
  <v-form>
    <h1>Upload an Image/ New Library</h1>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
  </v-form>
</template>
