import $http from '../utils/http.js'
import { Notification } from 'element-ui'
import router from '../router/index'
const GET_USER_LIST = 'usermanage/GET_USER_LIST'
const SET_USER_DATA = 'usermanage/SET_USER_DATA'
const RESET_USER_PASSWD = 'usermanage/RESET_USER_PASSWD'
const DETLET_USER_DATA = 'usermanage/DETLET_USER_DATA'
const GET_REPAIRE_DATA = 'usermanage/GET_REPAIRE_DATA'
const EDIT_USER_DATA = 'usermanage/EDIT_USER_DATA'
const SET_REPAIRE_DATA = 'usermanage/SET_REPAIRE_DATA'
const GET_SALES_REPAIRE = 'usermanage/GET_SALES_REPAIRE'
const SET_SALES_REPAIRE = 'usermanage/SET_SALES_REPAIRE'
export default {
    state: {
        pageNo: 1,
        name: '',        
        pageSize: 20,
        userData:[],
        total:0,
        tableDataRepaire:[],
        tableDataSale:[]
    },
    actions: {
        [GET_REPAIRE_DATA]({dispatch, commit, state}){
            $http.get('/api/recovery/user').then((data)=>{
                if(data.success){
                    commit(SET_REPAIRE_DATA, data.data)
                } else {
                    Notification.error('获取失败')
                    
                }
            })
        },
        [GET_SALES_REPAIRE]({dispatch, commit, state}){
            $http.get('/api/recovery/sale').then((data)=>{
                if(data.success){
                    commit(SET_SALES_REPAIRE, data.data)
                } else {
                    Notification.error('获取失败')
                    
                }
            })
        },
        [GET_USER_LIST]({ dispatch, commit, state }) {
            $http.get('/api/useinfo/list', {pageSize:state.pageSize, pageNo: state.pageNo, name: state.name}).then((data) => {
                if (data.success) {
                    commit(SET_USER_DATA, data)
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [RESET_USER_PASSWD]({ dispatch, commit, state }, obj) {
            $http.post('/api/userinfo/resetPassword', obj).then((data) => {
                if (data.success) {
                    dispatch(GET_USER_LIST)
                    Notification.success('重置成功')
                } else {
                    Notification.error('重置失败')
                }
            })
        },
        [DETLET_USER_DATA]({ dispatch, commit, state }, obj) {
            $http.post('/api/userinfo/delete', obj).then((data) => {
                if (data.success) {
                    dispatch(GET_USER_LIST)
                    Notification.success('删除成功')
                } else {
                    Notification.error('删除失败')
                }
            })
        },
        [EDIT_USER_DATA]({ dispatch, commit, state }, obj) {
            $http.post('/api/userinfo/add', obj).then((data) => {
                if (data.success) {
                    dispatch(GET_USER_LIST)
                    Notification.success('成功')
                } else {
                    Notification.error({
                        title: '提示',
                        message: data.msg
                    })
                }
            })
        },
    },
    mutations: {
        [SET_REPAIRE_DATA](state, data){
            state.tableDataRepaire = data
        },
        [SET_USER_DATA](state, data){
            state.userData = data.obj.result
            state.total = data.obj.totalCount
        },
        [SET_SALES_REPAIRE](state, data){
            state.tableDataSale = data
        }
    }
}
