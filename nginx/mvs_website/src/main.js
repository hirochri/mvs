import Vue from 'vue'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import store from './store.js'
import App from './App.vue'
import Home from './pages/Home.vue'
import About from './pages/About.vue'
import MyExperiments from './pages/MyExperiments.vue'
import Kickstarter from './pages/Kickstarter.vue'
import FileUpload from'./FileUpload.vue'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vue2-dropzone/dist/vue2Dropzone.css'

Vue.use(Vuetify)
Vue.use(VueRouter)

const routes = [
    { path: '/', component: Home },
    { path: '/about', component: About },
    { path: '/my-experiments', component: MyExperiments },
    { path: '/kickstarter', component: Kickstarter },
    { path: '/fileupload', component: FileUpload},
]

const router = new VueRouter({
    routes: routes,
})

var vm = new Vue({
    el: '#app',
    store: store,
    router: router,
    render: h => h(App)
})

global.vm = vm
