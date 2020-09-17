import axios from 'axios'
import {
  Message
} from 'element-ui'

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

var url = ''
axios.defaults.withCredentials = true // 跨域凭证

if(process.env.NODE_ENV == 'development'){
  url = '/'
  // console.log('aaa');
  // console.log(process.env.NODE_ENV);
  // console.log(process.env.VUE_APP_HOST);
}else{
  url = '/'
  // console.log('bbb');
  // console.log(process.env.NODE_ENV);
  // console.log(process.env.VUE_APP_HOST);
}
const instance = axios.create({
  baseURL: url,
  timeout: 5000
})
instance.all = axios.all

// 请求拦截器
instance.interceptors.request.use(function (request) {
  // 在发送请求之前做些什么
  const {
    params
  } = request
  return request
}, function (error) {
  if(error && error.response){
    var mess = ''
    switch (error.response.status) {
      case 400:
        mess = '错误请求，错误代码：400'
        break;
      case 401:
        mess = '未授权，请重新登录，错误代码：401'
        break;
      case 403:
        mess = '拒绝访问，错误代码：403'
        break;
      case 404:
        mess = '请求错误，未找到该资源，错误代码：404'
        break;
      case 405:
        mess = '请求方法未允许，错误代码：405'
        break;
      case 408:
        mess = '请求超时，错误代码：408'
        break;
      case 500:
        mess = '服务器端出错，错误代码：500'
        break;
      case 501:
        mess = '请网络未实现，错误代码：501'
        break;
      case 502:
        mess = '网络错误，错误代码：501'
        break;
      case 503:
        mess = '服务不可用，错误代码：501'
        break;
      case 504:
        mess = '网络超时，错误代码：501'
        break;
      case 505:
        mess = 'HTTP版本不支持该请求，错误代码：501'
        break;
    
      default:
        mess = `连接错误：${error.response.status}`
        break;
    }
  }else{
    mess = "连接到服务器失败"
  }
  return Promise.reject(mess)
  // 对请求错误做些什么
})

// 响应拦截器
instance.interceptors.response.use(function (response) {
  // 对响应数据做点什么
  return response
}, function (error) {
  // 对响应错误做点什么
  
  if (error.response.status === 500 || error.response.status === 404) {
    Message({
      message: '服务器拒绝连接，请重试',
      type: 'error'
    //   onClose() {
    //     // window.location.href = `${process.env.VUE_APP_API_HOST}auth/login`
    //   }
    })
  } else {
    Message({
      message: error.message,
      type: 'error',
      duration: 2 * 1000
    })
  }
  return Promise.reject(error)
})

export default instance
