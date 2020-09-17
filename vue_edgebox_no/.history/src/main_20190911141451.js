import Vue from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './vuex/store.js'
import './plugins/elementUI.js'
import axios from './plugins/axios'
import './style/index.scss'
import 'font-awesome/css/font-awesome.css'
import message from './message/message.js'

Vue.config.productionTip = false
Vue.prototype.$axios = axios // 设置全局变量
Vue.prototype.$Message = message

// 全局方法：按enter键搜索
Vue.prototype.confirmSubmit = function (event, func) {
  event.target.onkeydown = (e) => {
    console.log(e)
    if (e.keyCode === 13) {
      func()
    }
  }
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
