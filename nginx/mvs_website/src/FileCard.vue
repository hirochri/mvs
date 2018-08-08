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

      <v-container fluid>
        <v-checkbox v-for="vfunc in videoFunctions" v-bind:key="vfunc" v-model="selectedVideoFunctions" v-bind:label="vfunc" v-bind:value="vfunc"></v-checkbox>
      </v-container>

      <v-card-actions>
        <v-btn @click="confirmRemoveFunc" color="error">Delete Video</v-btn>
        <v-btn :loading="processing" :disabled="processing" color="success" @click.native="processFunc" >
          Process Video
          <span slot="loader">Processing...</span>
        </v-btn>
      </v-card-actions>

      <v-list v-if="processedVideos.length > 0">
        <v-subheader>Processed Videos</v-subheader>
        <v-card-text>
        <template v-for="video in processedVideos">
          <ul><a v-bind:href="video.link">{{video.name}}</a></ul>
        </template>
        </v-card-text>
      </v-list>




    </v-card>
  </div>
</template>

<script>
import axios from 'axios'

var mode = process.env.NODE_ENV || 'development'
var api_origin = (mode === 'production' ? '' : 'http://' + process.env.DEV_IP + ':3000')

//For static files, as it will break if testing/debugging outside of dockerland since nothing is serving the images
//Requires http server running in ../data/media (python -m http.server 8080)
var file_source = (mode === 'production') ? '/' : 'http://' + process.env.DEV_IP + ':8080/'

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
      processedVideos: [],
      videoFunctions: [],
      selectedVideoFunctions: [],
    }
  },
  props: ['file'],
  computed: {
    thumbnailSource: function() {
      return file_source + this.file.upload.uuid + "/thumbnail.jpg"
    },
    durationReadable: function () {
      var date = new Date(null)
      date.setSeconds(this.file.originalDuration)
      var timeString = date.toISOString().substr(11, 8)
      return timeString
    },
  },
  mounted () {
    axios.get(api_origin + '/api/video/functions/')
      .then(function(response) { //Handle success
        console.log(response.data)
        this.videoFunctions = response.data
      }.bind(this))
      .catch(function(error) { //Handle error
        if (error.response) { //Status code outside of 2xx range
          console.log(error.response.data, error.response.status, error.response.headers)
        } else if (error.request) { //Request made but no response received
          console.log(error.request)
        } else { //JS error in .then above
          console.log('Error', error.message)
        }
        this.videoFunctions = []
      }.bind(this))
  },
  methods: {
    confirmRemoveFunc: function() {
      if(confirm('Are you sure you want to remove ' + this.file.upload.filename + '?')){
        this.$emit('remove-file', this.file.upload.uuid)
      }
    },
    processFunc: function() {
      this.processing = true

      axios.post(api_origin + '/api/video/process/' + this.file.upload.uuid, {
        samplingRate: parseInt(this.samplingRate),
        samplingOption: parseInt(this.samplingOptionSelected),
        selectedVideoFunctions: this.selectedVideoFunctions
      })
        .then(function(response) { //Handle success
          // /uuid/rate_option.processed.mp4
          var video_link = file_source + this.file.upload.uuid + "/" + this.samplingRate + "_" + this.samplingOptionSelected + ".processed.mp4"
          var video_name = this.samplingRate + ' ' + this.samplingOptions[parseInt(this.samplingOptionSelected)].text
          this.processedVideos.push({'link': video_link, 'name': video_name})
        }.bind(this))
        .catch(function(error) { //Handle error
          if (error.response) { //Status code outside of 2xx range
            console.log(error.response.data, error.response.status, error.response.headers)
          } else if (error.request) { //Request made but no response received
            console.log(error.request)
          } else { //JS error in .then above
            console.log('Error', error.message)
          }
        }.bind(this))
        .then(function() { //Always executed
          this.processing = false
          this.selectedVideoFunctions = []
        }.bind(this))
    },
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


