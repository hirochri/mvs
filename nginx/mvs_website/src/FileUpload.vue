<template>
<div id="file-upload">
    <p>File Upload</p>
    <vue-dropzone id="dropzone" ref="dzone" v-bind:options="dropOptions"></vue-dropzone>
    <div>
        <li v-for="uf in uploaded_files">
            {{uf.upload.filename}}
        </li>
    </div>
</div>
</template>

<script>
import vueDropzone from "vue2-dropzone"

export default {
    data () {
        return {
            uploaded_files: [],
            dropOptions: {
                url: "http://127.0.0.1:3000/api/video/upload",
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
        vueDropzone
    },
    methods: {
        processFiles: function() {
            console.log(this.$refs.dzone.dropzone.files)
            this.$refs.dzone.processQueue()


        },
        successFunc: function(file, response) {
            console.log('dongs')
            console.log(this.uploaded_files)
            this.uploaded_files.push(file)
            this.$refs.dzone.removeFile(file)
        },
    }
}
</script>

<style></style>


