<template>
	<div id="file-card" class="card-div">
		<v-card>
			<div class="imgcontainer">
				<v-card-media v-bind:src="thumbnailSource" height="200px"></v-card-media>
				<div class="centered">
					<h3 class="headline mb-0">{{file.upload.filename}}</h3>
				</div>
				<div class="bottom-right">
					<h3 class="headline mb-0">{{durationReadable}}</h3>
				</div>
			</div>

			<v-text-field v-bind:placeholder="originalSamplingRate" v-model="samplingRate"></v-text-field>
			<v-select v-bind:items="samplingOptions" v-model="samplingOptionSelected" ></v-select>
			<v-card-actions>
				<v-btn @click="confirmRemoveFunc" color="error">Delete Video</v-btn>
				<v-btn :loading="processing" :disabled="processing" color="success" @click.native="processFunc" >
					Process Video
					<span slot="loader">Processing...</span>
				</v-btn>
			</v-card-actions>
		</v-card>
	</div>
</template>

<script>
import axios from 'axios'

var mode = process.env.NODE_ENV || 'development'
var api_origin = (mode === 'production' ? '' : 'http://' + process.env.DEV_IP + ':3000')

export default {
	data () {
		return {
			processing: false,
			originalSamplingRate: this.file.originalFps,
			samplingRate: this.file.originalFps,
			samplingOptionSelected: 0,
			samplingOptions: [
				{ text: 'Frames per second', value: 0 },
				{ text: 'Frames per minute', value: 1 },
				{ text: 'Frames per hour', value: 2 },
			],
		}
	},
	props: ['file'],
	computed: {
		thumbnailSource: function() {
			if (mode === 'development') {
				//Requires http server running in ../data/media (python -m http.server 8080)
				return 'http://' + process.env.DEV_IP + ':8080/' + this.file.upload.uuid + "/thumbnail.jpg"
			} else {
				//Will break if testing/debugging outside of dockerland since nothing is serving the images
				return "/" + this.file.upload.uuid + "/thumbnail.jpg"
			}
		},
    durationReadable: function () {
      var date = new Date(null)
      date.setSeconds(this.file.originalDuration)
      var timeString = date.toISOString().substr(11, 8)
      return timeString
    }
	},
	methods: {
		confirmRemoveFunc: function() {
			if(confirm('Are you sure you want to remove ' + this.file.upload.filename + '?')){
				this.$emit('remove-file', this.file.upload.uuid)
			}
		},
		processFunc: function() {
			this.processing = true

			console.log(this.file.upload.uuid)
			axios.post(api_origin + '/api/video/process/' + this.file.upload.uuid, {
				samplingRate: parseInt(this.samplingRate),
				samplingOption: parseInt(this.samplingOptionSelected)
			})
				.then(function(response) {
					//Handle success
					this.processing = false

				}.bind(this))
				.catch(function(error) {
					//Handle error
					this.processing = false
					console.log(JSON.stringify(error))
				}.bind(this))
				.then(function() {
					//Always executed

				})
		}
	}
}

</script>

<style>
.imgcontainer {
	position: relative;
	text-align: center;
	color: white;
}
.centered {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
}
.card-div {
  padding-right: 5px;
  padding-left: 5px;
  padding-bottom: 5px;
  padding-top: 5px;
}

.bottom-right {
    position: absolute;
    bottom: 8px;
    right: 16px;
}


</style>


