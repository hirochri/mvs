<template>
<div id="file-upload">
    <p>File Upload</p>
    <vue-dropzone id="drop1" :options="dropOptions"></vue-dropzone>
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
            }
        }
    },
    components: {
        vueDropzone

    }
}
</script>

<style></style>


