import axios from 'axios'
import {
  Message
} from 'element-ui'

axios.defaults.withCredentials = true // 跨域凭证

const instance = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api/' : process.env.VUE_APP_API_HOST,
  timeout: 5000
})

// 请求拦截器
instance.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  const {
    params
  } = request
  return config
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error)
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
      type: 'error',
      onClose () {
        // window.location.href = `${process.env.VUE_APP_API_HOST}auth/login`
      }
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
