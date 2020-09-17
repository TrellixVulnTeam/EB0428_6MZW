import Vue from 'vue'
import Router from 'vue-router'
import About from '../views/About.vue'
import Layout from '../views/Layout.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/Login',
      name: 'Login',
      component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue'),
      meta:{
        needLogin:false,
        title:'登录'
      },
    },
    {
      path: '/404',  
      name: '404',
      component: () => import(/* webpackChunkName: "about" */ '../components/404.vue'),
      meta:{
        needLogin:true,
        title:'页面不存在'
      },
    },
    {
      path: '/Retrieve',
      name: 'Retrieve',
      component: () => import(/* webpackChunkName: "about" */ '../components/Retrieve.vue'),
      meta:{
        needLogin:false,
        title:'忘记密码'
      },
    },
    {
      path: '/',
      name: 'Layout',
      // needLogin:true,
      component: Layout,
      children: [
        {
          path: '',
          name: 'test',
          component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue'),
          meta:{
            needLogin:true,
          },
          // component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceList.vue')
          // component: () => import(/* webpackChunkName: "about" */ '../views/test02.vue')
          // component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue')

        },
      ]
    },
    {
      path: '/index',
      name: 'Layout',
      component: Layout,
      meta:{
        needLogin:true,
        title:'首页'
      },
      children: [
        {
          path: '/SmallLogin',
          name: 'SmallLogin',
          component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue'),
          meta:{
            needLogin:false,
            title:'登录'
          },
        },
        {
          path: '',
          name: 'gatewaySysInfo',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/gatewayServer',
          name: 'gatewayServer',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayServer.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/gatewaySysInfo',
          name: 'gatewaySysInfo',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/gatewayList',
          name: 'gatewayList',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayList.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/deviceList',
          name: 'deviceList',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceList.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/deviceManage',
          name: 'deviceManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceManage.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/configuration',
          name: 'configuration',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/configuration.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/remoteManagement',
          name: 'remoteManagement',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/remoteManagement.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/logCenter',
          name: 'logCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/logCenter.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/eventCenter',
          name: 'eventCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/eventCenter.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/notificationManage',
          name: 'notificationManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/notificationManage.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/driver',
          name: 'driver', 
          component: () => import(/* webpackChunkName: "about" */ '../views/driverLibrary/driver.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/template',
          name: 'template',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/template.vue'),
          meta:{
            needLogin:true,
          },

        },
        {
          path: '/smartDevice',
          name: 'smartDevice', 
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartList.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/smartSetting',
          name: 'smartSetting',
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartSetting.vue'),
          meta:{
            needLogin:true,
          },
        },
        {
          path: '/centerUser',
          name: 'centerUser',
          component: () => import(/* webpackChunkName: "about" */ '../views/userCenter/userCenter.vue'),
          meta:{
            needLogin:true,
            title:'用户中心'
          },
        },
      ]
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    // }
  ]
})
