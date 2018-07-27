<template>
<div id="file-card">
    <v-layout>
    <v-flex xs12 sm6 offset-sm3>
    <v-card>
    <div class="imgcontainer">
        <v-card-media v-bind:src="thumbnailSource" height="200px"></v-card-media>
        <div class="centered">
            <h3 class="headline mb-0">{{file.upload.filename}}</h3>
        </div>
    </div>

    <!--
    <v-card-title primary-title>
    <h3 class="headline mb-0">{{file.upload.filename}}</h3>
    </v-card-title>
    -->

    <v-card-actions>
        <v-btn @click="confirmRemoveFunc" color="error">Delete Video</v-btn>
        <v-btn :loading="processing" :disabled="processing" color="success" @click.native="processFunc" >
            Process Video
            <span slot="loader">Processing...</span>
        </v-btn>
    </v-card-actions>

    </v-card>
    </v-flex>
    </v-layout>
</div>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            processing: false,
        }
    },
    props: ['file'],
    computed: {
        thumbnailSource: function() {
            //Python server running in /data/uploads until ngnix serves static
            return "http://127.0.0.1:8888/" + this.file.upload.uuid + ".thumbnail.jpg"
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
            axios.post('http://127.0.0.1:3000/api/video/process/' + this.file.upload.uuid)
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


</style>


