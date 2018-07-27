<template>
<div id="app">
    <v-app>
        <menu-bar></menu-bar>
        <!--
        <VuePerfectScrollbar class="scroll-area">
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </VuePerfectScrollbar>
        -->
        <div v-bar>
        <div>
                <router-view></router-view>
        </div>
        </div>

        <bottom-bar></bottom-bar>
    </v-app>
</div>
</template>
<script src="vuebar.js"></script>
<script>
import MenuBar from './MenuBar.vue'
import BottomBar from './BottomBar.vue'
import VuePerfectScrollbar from 'vue-perfect-scrollbar'

export default {
    data () {
        return {
        }
    },
    components: {
        'menu-bar': MenuBar, //Tag -> now registered component mapping
        'bottom-bar': BottomBar,
        'VuePerfectScrollbar': VuePerfectScrollbar,
    }
}
</script>

<style></style>
