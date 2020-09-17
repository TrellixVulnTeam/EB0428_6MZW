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
      path: '/index',
      name: 'Layout',
      component: Layout,
      children: [
        {
          path: '',
          name: 'gatewaySysInfo',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue')
        },
        {
          path: '/gatewayServer',
          name: 'gatewayServer',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayServer.vue')
        },
        {
          path: '/gatewaySysInfo',
          name: 'gatewaySysInfo',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewaySysInfo.vue')
        },
        {
          path: '/gatewayList',
          name: 'gatewayList',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gatewayList.vue')
        },
        {
          path: '/deviceList',
          name: 'deviceList',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceList.vue')
        },
        {
          path: '/deviceManage',
          name: 'deviceManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/deviceManage.vue')
        },
        {
          path: '/configuration',
          name: 'configuration',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/configuration.vue')
        },
        {
          path: '/remoteManagement',
          name: 'remoteManagement',
          component: () => import(/* webpackChunkName: "about" */ '../views/remotely/remoteManagement.vue')
        },
        {
          path: '/logCenter',
          name: 'logCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/logCenter.vue')
        },
        {
          path: '/eventCenter',
          name: 'eventCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/eventCenter.vue')
        },
        {
          path: '/notificationManage',
          name: 'notificationManage',
          component: () => import(/* webpackChunkName: "about" */ '../views/logManage/notificationManage.vue')
        },
        {
          path: '/driver',
          name: 'driver', 
          component: () => import(/* webpackChunkName: "about" */ '../views/driverLibrary/driver.vue')
        },
        {
          path: '/template',
          name: 'template',
          component: () => import(/* webpackChunkName: "about" */ '../views/chileDevice/template.vue')
        },
        {
          path: '/smartDevice',
          name: 'smartDevice', 
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartList.vue')
        },
        {
          path: '/smartSetting',
          name: 'smartSetting',
          component: () => import(/* webpackChunkName: "about" */ '../views/m5Module/smartSetting.vue')
        }
      ]
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    // }
  ]
})
