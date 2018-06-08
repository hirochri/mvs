<template>
<div id="app">
    <v-app>
        <menu-bar></menu-bar>
        <div style="background-color: red">a</div>
        <router-view></router-view>
        <div style="background-color: blue">a</div>
        <bottom-bar></bottom-bar>
    </v-app>
</div>
</template>

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
