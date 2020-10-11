import axios from 'axios'
import { stringify } from 'qs'
import router from '../router/index.js'

import { Notification } from 'element-ui'

let swicthTimeOut = false
const httpConfig = {
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Max-Age': '86400',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
    'Access-Control-Allow-Headers': 'token, host, x-real-ip, x-forwarded-ip, accept, content-type'
  }
}
axios.interceptors.response.use(function (response) {
  // Do something with response data
  if (response.headers['content-disposition'] != undefined) {
    return response
  } else if (response.status >= 400) { return Promise.reject('400+Error') } else {
    try {
      var resp = response.data
      if (resp.status === 'timeout') {
        router.push('/login')
        portalRouter.push('/login')
        exchangeRouter.push('/login')
        if (swicthTimeOut === false) {
          swicthTimeOut = true
          Notification.error({
            title: '因长时间未操作,请重新登录'
          })
        }
        return Promise.reject('timeout')
      } else if (resp.status === 'notallow') {
        Notification.error({
          title: '当前用户无权限进行此操作'
        })
      } else {
        swicthTimeOut = false
        if (resp.status !== 'success' && resp.status !== 'default' && resp.status !== 'timeout' && resp.status !== 'notallow') resp.status = 'fail'
        return resp
      }
    } catch (e) {
      console.log(e)
    }
  }
}, function (error) {
  // Do something with response error
  console.log(error)
  return Promise.reject(error)
})

const $http = (url, option = {}, header = {}) => {
  return axios
    .request({ url, headers: { ...httpConfig.headers, ...header }, ...option })
    .catch(function (e) {
      console.log(e)
    })
}

const httpMiddleware = {
  get: (url, param = {}) => $http(`${url}?${stringify({ ...param, _k: new Date().getTime() })}`, { method: 'GET' }),
  post: (url, param = {}) => $http(url, { method: 'POST', data: stringify({ ...param, _k: new Date().getTime() }) }),
  put: (url, param = {}) => $http(url, { method: 'PUT', data: stringify({ ...param, _k: new Date().getTime() }) }),
  delete: (url, param = {}) => $http(`${url}?${stringify({ ...param, _k: new Date().getTime() })}`, { method: 'DELETE' }),
  option: (url, param = {}, header = { 'Content-Type': 'application/json' }) => $http(url, { method: 'POST', data: param }, header)
}

export default httpMiddleware
