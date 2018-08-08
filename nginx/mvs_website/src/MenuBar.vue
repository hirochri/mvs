<template>
<div id="menu-bar">
    
    <v-tabs dark color="grey darken-3" right>
        <v-tab v-for="(route, item) in menu_items" v-bind:to="route" v-bind:key="item">
        {{item}}
        </v-tab>
        <!--
        <div color="red">
            {{$store.state.count}}
            {{evenOrOdd}}
        </div>
        <button @click="increment">+</button>
        <button @click="decrement">-</button>
        <input v-on:keyup.enter="set_count" type="text">
        -->

    </v-tabs>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
    data () {
        return {
            menu_items: {
                "Home": "/",
                "About": "/about",
                "File Upload": "/fileupload",
                "My Experiments": "/my-experiments",
                "Kickstarter": "/kickstarter",
            },
        }
    },
    computed: mapGetters([
        'evenOrOdd'
    ]),
    methods: mapActions([
        'increment',
        'decrement',
        'set_count'
    ])
}
</script>

<style></style>
