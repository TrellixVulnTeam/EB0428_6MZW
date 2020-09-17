import Vue from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './vuex/store.js'
import './plugins/Vant.js'
import './style/index.scss'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
