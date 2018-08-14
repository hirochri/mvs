<template>
<div id="">
    <v-layout row flex>
            <img v-bind:src="logoSource">

              <v-card-text>
              <strong>Drosophila Project</strong>
              </br>
              </br>
              The Drosophila is a microscopic video surveillance system inspired my nature. It is intended to utilize the power of modern surveillance for live cell imaging applications. It is a compact, high performance, affordable system that is made possible by proprietary design and engineering. ​
              </br>
              </br>
              Our technology is a modular, inexpensive, climate proof surveillance system that can be placed inside of a standard incubator for live cell imaging applications. Each system contains multiple imaging modules, where each module contains an independently controlled digital video microscope. The modules are arranged on a universal platform which collects data from the modules, and delivers the data remotely to cloud servers, so that videos can be remotely viewed and analyzed anywhere, and anytime. ​
              </br>
              </br>
              <strong>DONATION</strong>
              </br>
              Donate to the Drosophila Kickstarter Project at www.kickstarter.com/
              </v-card-text>

    </v-layout>
</div>
</template>

<script>
var mode = process.env.NODE_ENV || 'development'
var file_source = (mode === 'production') ? './assets/' : './'
if (mode === 'development') {
  var images = require.context('../assets/', false, /\.(jpg|png)$/)

  //https://stackoverflow.com/questions/40491506/vue-js-dynamic-images-not-working
  //https://github.com/vuejs-templates/webpack/issues/267
  //^Some info on this puzzling problem with dynamic filenames
}
export default {
    data () {
        return {
        }
    },
    computed: {
      logoSource: function() {
        if (mode === 'production') {
          return file_source + "drosophila_logo_transparent.png"
        } else {
          return images(file_source + "drosophila_logo_transparent.png")
        }
      }
  }
}
</script>

<style></style>


