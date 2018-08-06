<template>
	<div id="file-upload">
		<vue-dropzone id="dropzone" ref="dzone" v-bind:options="dropOptions"></vue-dropzone>
		<v-container fluid grid-list-md>
			<v-layout row wrap flex align-center>
				<file-card v-for="cf in current_files" v-bind:key="cf.upload.uuid" v-bind:file="cf" v-on:remove-file="removeFunc"></file-card>
			</v-layout>
		</v-container>
	</div>
</template>

<script>
import vueDropzone from "vue2-dropzone"
import FileCard from './FileCard.vue'
import axios from 'axios'

var mode = process.env.NODE_ENV || 'development'
var api_origin = (mode === 'production' ? '' : 'http://' + process.env.DEV_IP + ':3000')
//Nginx sends anything with /api/ to the app container due to config
//Using localhost works with flask + frontend, but mongo also needs to be running locally

export default {
	data () {
		return {
			current_files: [],
			dropOptions: {
				url: api_origin + "/api/video/upload",
				maxFilesize: 100, //mb, #nginx also has 100mb limit
				maxFiles: 10,
				addRemoveLinks: true,
				parallelUploads: 2,
				sending: function(file, xhr, formData){
					formData.append('uuid', file.upload.uuid);
				},
				success: this.successFunc,
			},
		}
	},
	components: {
		'vueDropzone': vueDropzone,
		'file-card': FileCard,
	},
	methods: {
		removeFunc: function(uuid) {
			this.current_files = this.current_files.filter(function(file) {
				return file.upload.uuid !== uuid
			})

			axios.delete(api_origin + '/api/video/remove/' + uuid)
				.then(res => {
					console.log(res)
				})
		},
		successFunc: function(file, response) {
      var jresponse = JSON.parse(response)
			file.originalFps = jresponse['fps']
      file.originalDuration = jresponse['duration']
			this.current_files.push(file)
			this.$refs.dzone.removeFile(file)
		},
	}
}
</script>

<style></style>






