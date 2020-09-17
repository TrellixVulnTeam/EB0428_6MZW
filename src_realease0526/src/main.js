import Vue from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './vuex/store.js'
import './plugins/elementUI.js'
import axios from './plugins/axios'
import './style/index.scss'
import 'font-awesome/css/font-awesome.css'
import message from './message/message.js'
import cookie from './until/cookie.js'
import secre from './until/secretKey.js'
import echarts from 'echarts'
import highCharts from 'highcharts/highstock'
import JsonViewer from 'vue-json-viewer'
import screenfull from 'screenfull'
import phone from './until/phone'
import sparkMD5 from 'spark-md5'
import $ from 'jquery' 
// import '@babel/polyfill';
// import Es6Promise from 'es6-promise'
import md5 from 'js-md5';
let Base64 = require('js-base64').Base64;
// Es6Promise.polyfill()
require('highcharts/modules/exporting')(highCharts);
Vue.use(JsonViewer)
Vue.config.productionTip = false
Vue.prototype.$axios = axios // 设置全局变量
Vue.prototype.$Message = message
Vue.prototype.$echarts = echarts
Vue.prototype.$highCharts = highCharts
Vue.prototype.$md5 = md5
Vue.prototype.$cookie = cookie
Vue.prototype.$secre = secre
Vue.prototype.$screenfull = screenfull
Vue.prototype.$phone = phone
Vue.prototype.$sparkMD5 = sparkMD5

// 全局方法：按enter键搜索
Vue.prototype.confirmSubmit = function (event, func) {
  event.target.onkeydown = (e) => {
    console.log(e)
    if (e.keyCode === 13) {
      func()
    }
  }
}

// highCharts.setOptions({
//   global: {
//           useUTC: false
//   },
// })

router.beforeEach(function(to, from, next) {
  // console.log(to);
  // console.log(to.fullPath);
  if(to.meta.title != null){
    document.title = to.meta.title
  }
  if (to.meta.needLogin == true) {
    // console.log("需要登陆");
    //页面是否登录
    if (localStorage.getItem("tokenLogin")) {
      // console.log("token存在:" + localStorage.getItem("token"));
      //本地存储中是否有token(uid)数据
      var nowTime = new Date().getTime()
      
      var json = JSON.parse(secre.changeSecret(localStorage.getItem("tokenLogin")))
      var time = nowTime - json["date"]
      var isLogin = json["isLogin"]
      if(isLogin == true || time <= (60 * 60 * 1000)){
        next()
      }else{
        // localStorage.removeItem("tokenLoin")
        Vue.prototype.$Message.ErrorMessage(Vue.prototype, "登陆超时，请重新登录")
        next({
          name: "SmallLogin"
        });
      }
      // console.log(json);
      console.log(time);
    } else {
      // console.log("token不存在");
      //next可以传递一个路由对象作为参数 表示需要跳转到的页面
      next({
        name: "Login"
      });
    }
  } else if(to.meta.needLogin == false) {
    // console.log("不需要登陆");
    next(); //继续往后走
    //表示不需要登录
  }else{
    next({
      name: "404"
    })
  }
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

