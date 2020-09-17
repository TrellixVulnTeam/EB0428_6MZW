import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home.vue'
import Container from '../views/Container.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Container',
      component: Container
    },
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
      path: '/test',
      name: 'test',
      component: () => import(/* webpackChunkName: "about" */ '../views/test.vue')
    }
  ]
})
