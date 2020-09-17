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
      path: '/',
      name: 'Layout',
      component: Layout,
      children: [
        {
          path: '',
          name: 'test',
          // component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceList.vue')
          // component: () => import(/* webpackChunkName: "about" */ '../views/test02.vue')
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue')

        },
      ]
    },
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
        needLogin:false,
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
            title:'系统信息'
          },
        },
        {
          path: '/gatewayServer',
          name: 'gatewayServer',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayServer.vue'),
          meta:{
            needLogin:true,
            title:'网关服务'
          },
        },
        {
          path: '/gatewaySysInfo',
          name: 'gatewaySysInfo',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue'),
          meta:{
            needLogin:true,
            title:'系统信息'
          },
        },
        {
          path: '/gatewayList',
          name: 'gatewayList',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayList.vue'),
          meta:{
            needLogin:true,
            title:'网关信息'
          },
        },
        {
          path: '/deviceList',
          name: 'deviceList',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceList.vue'),
          meta:{
            needLogin:true,
            title:'子设备列表'
          },
        },
        {
          path: '/deviceManage',
          name: 'deviceManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceManage.vue'),
          meta:{
            needLogin:true,
            title:'子设备管理'
          },
        },
        {
          path: '/configuration',
          name: 'configuration',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/configuration.vue'),
          meta:{
            needLogin:true,
            title:'配置下发'
          },
        },
        {
          path: '/remoteManagement',
          name: 'remoteManagement',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/remoteManagement.vue'),
          meta:{
            needLogin:true,
            title:'远程管理'
          },
        },
        {
          path: '/logCenter',
          name: 'logCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/logCenter.vue'),
          meta:{
            needLogin:true,
            title:'日志中心'
          },
        },
        {
          path: '/eventCenter',
          name: 'eventCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/eventCenter.vue'),
          meta:{
            needLogin:true,
            title:'事件中心'
          },
        },
        {
          path: '/notificationManage',
          name: 'notificationManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/notificationManage.vue'),
          meta:{
            needLogin:true,
            title:'通知管理'
          },
        },
        {
          path: '/driver',
          name: 'driver', 
          component: () => import(/* webpackChunkName: "about" */ '../views/driverLibrary/driver.vue'),
          meta:{
            needLogin:true,
            title:'驱动库'
          },
        },
        {
          path: '/template',
          name: 'template',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/template.vue'),
          meta:{
            needLogin:true,
            title:'模板库'
          },
        },
        {
          path: '/smartDevice',
          name: 'smartDevice', 
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartList.vue'),
          meta:{
            needLogin:true,
            title:'智能设备列表'
          },
        },
        {
          path: '/smartSetting',
          name: 'smartSetting',
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartSetting.vue'),
          meta:{
            needLogin:true,
            title:'即插即用设置'
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

  ]
})
