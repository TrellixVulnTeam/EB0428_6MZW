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
      name: 'About',
      component: About
    },
    {
      path: '/layout',
      name: 'Layout',
      component: Layout,
      children: [
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
          name: 'deviceList',
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
