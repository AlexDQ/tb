import system from './system.js'
import location from './location.js'
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
export default new Vuex.Store({
    modules: {
      system,
      location
    }
  })