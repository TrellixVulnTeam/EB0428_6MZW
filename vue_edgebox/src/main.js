import Vue from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './vuex/store.js'
// import JSONView from './plugins/jsonview.js'
import "@/plugins/jsonview.js"
import './plugins/elementUI.js'
import '@/plugins/echarts.js'
import axios from './plugins/axios'
import './style/index.scss'
import 'font-awesome/css/font-awesome.css'
import message from './message/message.js'
// import echarts from 'echarts'
import JsonViewer from 'vue-json-viewer'
// import $ from 'jquery' 
// import md5 from 'js-md5';
// let Base64 = require('js-base64').Base64;

Vue.use(JsonViewer)
Vue.config.productionTip = false
Vue.prototype.$axios = axios // 设置全局变量
Vue.prototype.$Message = message
// Vue.prototype.$echarts = echarts
// Vue.prototype.$md5 = md5

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
  // JSONView,
  render: h => h(App)
}).$mount('#app')
