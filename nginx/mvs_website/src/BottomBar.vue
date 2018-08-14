<template>
  <div id="bottom-bar">
    <v-footer dark color="grey darken-3" height="auto">
      <v-container>
        <v-layout>
          <v-flex>
            Contact:<br>
            <br>
            <br>
          </v-flex>
          <v-flex>
            Alexis Donneys<br>
            215-219-8748<br>
            alexisd@med.umich.edu<br>
          </v-flex>
          <v-flex>
            109 Zina Pitcher Pl<br>
            2638 Biomedical Science Research Building<br>
            Ann Arbor, MI 48109<br>
          </v-flex>

          <v-layout justify-space-around>
            <v-btn fab depressed small color="grey darken-3" v-for="icon in icons" v-bind:name="icon" v-bind:key="icon">
              <icon v-bind:name="icon"></icon>

            </v-btn>
          </v-layout>

          <v-btn color="primary" @click.native.stop="dialog = true">Message MVS</v-btn>
          <v-dialog max-width="500px" v-model="dialog" @keydown.esc="dialog = false">
            <v-card>
              <v-card-title>
                <span class="headline">Contact Alexis Donneys</span>
              </v-card-title>
              <v-card-text>
                <v-form @submit.prevent="handleSubmit">
                  <v-text-field label="Name" required v-model="contact.name"></v-text-field>
                  <v-text-field label="Email" required v-model="contact.email"></v-text-field>
                  <v-text-field label="Subject" v-model="contact.subject"></v-text-field>
                  <v-text-field label="Message" textarea multi-line rows="2" v-model="contact.message"></v-text-field>
                  <v-layout align-end justify-end>
                    <v-btn depressed type="submit" @click="dialog = false">Submit</v-btn>
                  </v-layout>
                </v-form>
              </v-card-text>
            </v-card>
          </v-dialog>


        </v-layout>
      </v-container>
    </v-footer>
  </div>
</template>

<script>
import axios from 'axios'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'


export default {
  data () {
    return {
      dialog: false,
      icons: [
        'brands/facebook-f',
        'brands/twitter',
        'brands/instagram',
        'brands/youtube',
        'brands/google-plus-g'
      ],
      contact: {
        name: '',
        email: '', 
        subject: '',
        message: ''
      }
    }
  },
  components: {
    Icon
  },
  methods: {
    handleSubmit(event) {
      //Handle email validation client side
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

<style>
</style>


