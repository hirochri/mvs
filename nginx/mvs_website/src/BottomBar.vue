<template>
<div id="bottom-bar">
    <v-footer height="auto" v-bind:absolute="true">
        <v-container>
            <v-layout>
            <v-flex xs4>
                Contact
                Alexis Donneys
                215-219-8748
                alexisd@med.umich.edu
            </v-flex>
            <v-flex xs4>
                109 Zina Pitcher Pl
                2638 Biomedical Science Research Building
                Ann Arbor, MI 48109
            </v-flex>

            <v-flex xs4>
                <v-btn v-for="icon in icons" v-bind:key="icon" icon>
                    <v-icon>{{icon}}</v-icon>
                </v-btn>
            </v-flex>

            <v-btn color="primary" @click.native.stop="dialog = true">Message MVS</v-btn>
            <v-dialog v-model="dialog" @keydown.esc="dialog = false">
                <v-card>
                    <v-form @submit.prevent="handleSubmit">
                        <v-text-field label="Name" required v-model="contact.name"></v-text-field>
                        <v-text-field label="Email" required v-model="contact.email"></v-text-field>
                        <v-text-field label="Subject" v-model="contact.subject"></v-text-field>
                        <v-text-field label="Message" textarea multi-line rows="2" v-model="contact.message"></v-text-field>
                        <button type="submit" @click="dialog = false">Submit</button>
                    </v-form>
                </v-card>
            </v-dialog>

            </v-layout>
        </v-container>
    </v-footer>
</div>
</template>

<script>
import axios from 'axios'
export default {
    data () {
        return {
            dialog: false,
            icons: [
                'fa fa-facebook',
                'fa fa-twitter',
                'fa fa-instagram',
                'fa fa-youtube',
                'fa fa-google-plus'
            ],
            contact: {
                name: 'yung lean',
                email: '', 
                subject: '',
                message: ''
            }
        }
    },
    methods: {
        handleSubmit(event) {
            //Handle email validation client side
            console.log("ayy")
            console.log(event)
            console.log(this.contact.name)
            axios.post('http://127.0.0.1:3000/api/contact/', this.contact)
            .then(res => {
                console.log(res)
            })
        }
    }
}
</script>

<style></style>


