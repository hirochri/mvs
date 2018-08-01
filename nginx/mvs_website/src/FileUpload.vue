<template>
<div id="file-upload">
    <p>File Upload</p>
    <vue-dropzone id="dropzone" ref="dzone" v-bind:options="dropOptions"></vue-dropzone>
    <div>
        <p>Current files</p>
        <div>
            <file-card v-for="cf in current_files" v-bind:key="cf.upload.uuid" v-bind:file="cf" v-on:remove-file="removeFunc"></file-card>
        </div>
    </div>
</div>
</template>

<script>
import vueDropzone from "vue2-dropzone"
import FileCard from './FileCard.vue'
import axios from 'axios'

var mode = process.env.NODE_ENV || 'development'
var api_origin = (mode === 'production' ? '' : 'http://127.0.0.1:3000')
//Nginx sends anything with /api/ to the app container due to config

export default {
    data () {
        return {
            current_files: [],
            dropOptions: {
                url: api_origin + "/api/video/upload",
                maxFilesize: 50, //mb,
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
            console.log(file)
            file.originalFps = parseInt(response)
            this.current_files.push(file)
            this.$refs.dzone.removeFile(file)
        },
    }
}
</script>

<style></style>


