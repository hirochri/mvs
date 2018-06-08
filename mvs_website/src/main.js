import Vue from 'vue'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import App from './App.vue'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify)
Vue.use(VueRouter)

const Home = { template: '<div>Home</div>' }
const About = { template: '<div>About</div>' }


const routes = [
    { path: '/home', component: Home },
    { path: '/about', component: About},
]

const router = new VueRouter({
    routes: routes,
})

new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
})
