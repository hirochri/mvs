<template>
<div id="menu-bar">
    <v-tabs right>
        <v-tab v-for="(route, item) in menu_items" v-bind:to="route" v-bind:key="item">
        {{item}}
        </v-tab>
    </v-tabs>
</div>
</template>

<script>
export default {
    data () {
        return {
            menu_items: {
                "Home": "/",
                "About": "/about",
                "Services": "/services",
                "Locations": "/locations",
                "My Experiments": "/my-experiments",
                "Kickstarter": "/kickstarter",
                "Contact": "/contact"
            },
        }
    }
}
</script>

<style></style>
