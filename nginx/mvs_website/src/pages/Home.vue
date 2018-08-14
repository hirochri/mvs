<template>
  <div id="home-page" v-bind:style="backgroundStyle">
    <img v-bind:src='logoSource'/>

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
        return file_source + "mvs_logo_white.png"
      } else {
        return images(file_source + "mvs_logo_white.png")
      }
    },
    backgroundSource: function() {
      if (mode === 'production') {
        return file_source + "stem_cell2.jpg"
      } else {
        return images(file_source + "stem_cell2.jpg")
      }
    },
    backgroundStyle: function() {
      return {
        'height': '100%',
        'width': '100%',
        'background-image': 'url("' + this.backgroundSource + '")',
        'background-position': 'center',
        'background-size': 'cover'
      }

    }
  }
}
//The CSS is a little wonky especially when the window size changes.. 
//Probably just a temp solution for now
</script>

<style>

#home-page img {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

}
</style>


