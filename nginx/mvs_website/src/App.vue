<template>
<div id="app">
    <v-app>
        <menu-bar></menu-bar>
        <VuePerfectScrollbar class="scroll-area">
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </VuePerfectScrollbar>
        <bottom-bar></bottom-bar>
    </v-app>
</div>
</template>
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
