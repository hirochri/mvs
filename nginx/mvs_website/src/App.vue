<template>
<div id="app">
    <v-app>
        <menu-bar></menu-bar>
        <router-view></router-view>
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
        'menu-bar': MenuBar, //Tag -> now registered component mapping
        'bottom-bar': BottomBar,
    }
}
</script>

<style></style>
