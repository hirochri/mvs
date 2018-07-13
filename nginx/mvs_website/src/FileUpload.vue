<template>
<div id="file-upload">
    <p>File Upload</p>
    <vue-dropzone id="dropzone" ref="dzone" v-bind:options="dropOptions"></vue-dropzone>
    <v-btn v-on:click="processFiles">Upload and process</v-btn>
</div>
</template>

<script>
import vueDropzone from "vue2-dropzone"

export default {
    data () {
        return {
            dropOptions: {
                url: "http://127.0.0.1:3000/api/video/",
                maxFilesize: 50, //mb,
                maxFiles: 10,
                uploadMultiple: true,
                addRemoveLinks: true,
                autoProcessQueue: false,
                parallelUploads: 1,
                success: function(file, response) {
                    console.log(file)
                    console.log(typeof(response))

                },
            }
        }
    },
    components: {
        vueDropzone

    },
    methods: {
        processFiles: function() {
            console.log(this.$refs.dzone.dropzone.files)
            this.$refs.dzone.processQueue()


        }
    }
}
</script>

<style></style>


