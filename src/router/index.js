import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/containers/login.vue'
import locationAnalysis from '@/containers/locationAnalysis.vue'
import dataAnalysis from '@/containers/dataAnalysis.vue'
import dataManagement from '@/containers/dataManagement.vue'

import Layout from '@/containers/layout.vue'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: '登录',
      component: Login
    },
    {
      path: '/platform',
      name: 'layout',
      component: Layout,
      children: [
        {
          path: '/locationAnalysis',
          name: '地理位置分析',
          component: locationAnalysis
        },
        {
          path: '/dataAnalysis',
          name: '销售数据分析',
          component: dataAnalysis
        },
        {
          path: '/dataManagement',
          name: '销售数据管理',
          component: dataManagement
        },
      ]
    }
  ]
})
