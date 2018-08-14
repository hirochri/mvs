<template>
<div id="about-page">
    <v-card-text>
    <strong>About Us:</strong>
    In modern biomedical research there is a high demand for real-time video microscopy, yet an access bottleneck exists due to a combination of the large size, complexity and high cost of existing commercial systems. Our goal is to make live cell imaging accessible for the masses. In order to do this, we have established online services to connect investigators with our emerging live cell imaging technologies and facilities. In addition, we are currently developing an easy to use, affordable, high performance commercial system that will put the power of live cell imaging surveillance within reach for the modern-day investigator.  
    </v-card-text>
    <v-card-text>
    <strong>Services: </strong>
    The Microscopic Video Surveillance (MVS) project promotes the use of surveillance technology for live cell imaging microscopy. This technology enables investigators to record video footage of multiple live cell cultures simultaneously, in a standard incubator over extended periods of time. Our MVS system features up to six inverted light microscope cameras (200x total magnification) with remote stage movement control and focusing manipulations (x, y, and z plane), as well as surveillance capabilities from a remote location. Real-time recordings are accessible from a Mac/PC or handheld device. Video editing and data generation services are available for an additional cost.

    </br>
    </br>
    Service Fee: $29.50 per hour for Cell experiments, MVS Use, Video Editing, Data Generation and Analysis
    </v-card-text>
    <img v-for="service in serviceSources" v-bind:src="service">

    <v-card-text>
    <strong>Locations: </strong>
    Our services are offered online at www.MVScorefacility.com, as well as at these University-based core facilities: University of Michigan, BSRB, NCRC 
    </v-card-text>
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
      serviceSources: function() {
        if (mode === 'production') {
          return [file_source + 'service1.jpg', file_source + 'service2.jpg', file_source + 'service3.jpg']
        } else {
          return [images(file_source + 'service1.jpg'), images(file_source + 'service2.jpg'), images(file_source + 'service3.jpg')]
        }
      }

    },
}

</script>

<style></style>


