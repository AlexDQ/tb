import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/containers/login.vue'
import infoManagement from '@/containers/infoManagement.vue'
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
          path: '/infoManagement',
          name: '个人信息管理',
          component: infoManagement
        },
        {
          path: '/locationAnalysis',
          name: '个人信息管理',
          component: infoManagement
        },
      ]
    }
  ]
})
