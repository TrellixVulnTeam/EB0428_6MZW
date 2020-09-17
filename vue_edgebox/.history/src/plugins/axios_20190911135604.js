import axios from 'axios'
import { Message } from 'element-ui'

axios.defaults.withCredentials = true // 跨域凭证


const instance = axios.create({
    baseURL: process.env.NODE_ENV === 'development' ? '/api/' : process.env.VUE_APP_API_HOST,
})
