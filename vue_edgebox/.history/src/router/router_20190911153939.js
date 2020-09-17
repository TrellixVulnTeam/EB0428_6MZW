import Vue from 'vue'
import Router from 'vue-router'
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
          path: '/gateList',
          name: 'gateList',
          component: () => import(/* webpackChunkName: "about" */ '../views/gatewayManage/gateList.vue')
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
