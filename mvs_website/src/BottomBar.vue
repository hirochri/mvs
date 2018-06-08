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
            <v-dialog v-model="dialog">
                <v-card>
                    <v-form>
                        <v-text-field label="Name" required></v-text-field>
                        <v-text-field label="Email" required></v-text-field>
                        <v-text-field label="Subject"></v-text-field>
                        <v-text-field label="Message" textarea multi-line rows="2"></v-text-field>
                    </v-form>
                </v-card>
            </v-dialog>

            </v-layout>
        </v-container>
    </v-footer>
</div>
</template>

<script>
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
        }
    }
}
</script>

<style></style>


