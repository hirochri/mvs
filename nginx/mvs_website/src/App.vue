<template>
<div id="app">
    <v-app>
      <menu-bar></menu-bar>
      <v-flex fill-height>
        <router-view></router-view>
      </v-flex>
      <bottom-bar></bottom-bar>
    </v-app>
</div>
</template>
<script src="vuebar.js"></script>
<script>
import MenuBar from './MenuBar.vue'
import BottomBar from './BottomBar.vue'

export default {
    data () {
        return {
        }
    },
    components: {
        'menu-bar': MenuBar,
        'bottom-bar': BottomBar,
    }
}
</script>

<style> </style>
