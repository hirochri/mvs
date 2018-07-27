<template>
<div id="file-card">
    <v-layout>
        <v-flex xs12 sm6 offset-sm3>
            <v-card>
                <!--
                <v-card-media
                 src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
                 height="200px"
                 ></v-card-media>
                 -->

                <v-card-title primary-title>
                <h3 class="headline mb-0">{{file.upload.filename}} {{file.upload.uuid}}</h3>
                </v-card-title>

                <!--
                <v-card-actions>
                <v-btn flat color="orange">Share</v-btn>
                <v-btn flat color="orange">Explore</v-btn>
                </v-card-actions>
                -->
                <button @click="$emit('remove-file', file.upload.uuid)">DELETE</button>
                <button @click="processFunc">PROCESS</button>
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
        }
    },
    props: ['filename', 'file'],
    methods: {
        processFunc: function() {
            axios.post('http://127.0.0.1:3000/api/video/process/', this.file.upload.uuid)
            .then(res => {
                console.log(res)
            })
        }
    }
}

</script>

<style></style>


