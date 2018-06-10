import Vue from 'vue'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import store from './store.js'
import App from './App.vue'
import Home from './pages/Home.vue'
import About from './pages/About.vue'
import Services from './pages/Services.vue'
import Locations from './pages/Locations.vue'
import MyExperiments from './pages/MyExperiments.vue'
import Kickstarter from './pages/Kickstarter.vue'
import Contact from './pages/Contact.vue'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify)
Vue.use(VueRouter)

const routes = [
    { path: '/', component: Home },
    { path: '/about', component: About },
    { path: '/services', component: Services },
    { path: '/locations', component: Locations },
    { path: '/my-experiments', component: MyExperiments },
    { path: '/kickstarter', component: Kickstarter },
    { path: '/contact', component: Contact },
]

const router = new VueRouter({
    routes: routes,
})

new Vue({
    el: '#app',
    store: store,
    router: router,
    render: h => h(App)
})
