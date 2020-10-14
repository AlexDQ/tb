import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/containers/login.vue'
import locationAnalysis from '@/containers/locationAnalysis.vue'
import dataAnalysis from '@/containers/dataAnalysis.vue'
import dataManagement from '@/containers/dataManagement.vue'
import behaviorAnalysis from '@/containers/behaviorAnalysis.vue'
import userManagement from '@/containers/userManagement.vue'
import Layout from '@/containers/layout.vue'
import dataRepair from '@/containers/dataRepair.vue'
import salesRepair from '@/containers/salesRepair.vue'


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
        {
          path: '/behaviorAnalysis',
          name: '销售数据管理',
          component: behaviorAnalysis
        },
        {
          path: '/userManagement',
          name: '用户管理',
          component: userManagement
          
        },
        {
          path: '/dataRepair',
          name: '数据恢复',
          children:[
            {
              path: '/salesRepair',
              name: '数据恢复',
              component: salesRepair
            },
            {
              path: '/userRepair',
              name: '用户恢复',
              component: dataRepair
            }
          ]
        },
      ]
    }
  ]
})