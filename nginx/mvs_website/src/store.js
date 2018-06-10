import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        count: 0
    },
    getters: {
        evenOrOdd: function(state) {
            return state.count % 2 === 0 ? 'even' : 'odd'
        }
    },
    //"setters", but not used directly
    mutations: {
        increment: function(state) {
            state.count++

        },
        decrement: function(state) {
            state.count--
        },
        set_count: function(state, payload) {
            state.count = payload

        }
    },
    actions: {
        increment: function(context) {
            context.commit('increment')
        },
        decrement: function(context) {
            context.commit('decrement')
        },
        set_count: function(context, payload) {
            //Here the keyup.enter event comes in as "payload"
            console.log(payload.target.value)
            console.log(typeof payload.target.value)
            context.commit('set_count', parseInt(payload.target.value, 10))

        }
    }
})
