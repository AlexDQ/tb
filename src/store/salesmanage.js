import $http from '../utils/http.js'
import { Notification } from 'element-ui'
const GET_TABLE_DATA = 'salesmanage/GET_TABLE_DATA'
const SET_TABLE_DATA = 'salesmanage/SET_TABLE_DATA'
const DOWNLOAD_CSV_DATA = 'salesmanage/DOWNLOAD_CSV_DATA'
const GET_CHART_DATA = 'salesmanage/GET_CHART_DATA'
const SET_CHART_DATA = 'salesmanage/SET_CHART_DATA'
const SUBMIT_FORM_DATA = 'salesmanage/SUBMIT_FORM_DATA'
const GET_PIE_DATA = 'salesmanage/GET_PIE_DATA'
const SET_PIE_DATA = 'salesmanage/SET_PIE_DATA'
const GET_BEHAVIOR_DATA = 'salesmanage/GET_BEHAVIOR_DATA'
const SET_BEHAIVOR_DATA = 'salesmanage/SET_BEHAIVOR_DATA'
const DELETE_BEHAVIOR_DATA = 'salesmanage/DELETE_BEHAVIOR_DATA'
const ADD_BEHAVIOR_DATA = 'salesmanage/ADD_BEHAVIOR_DATA'
export default{
    state:{
        tableData:[],
        form:{
            behavior_type:'',
            item_id: '',
            item_category: ''
        },
        showFlag: false,
        showFlag1: false,
        xdata: [],
        ydata: [],
        piexdata:[],
        pieydata:[],
        behaviorData: [],
        dataform :{
            user_id: '',
            item_id: '',
            behavior_type: '',
            longitude: '',
            latitude:'',
            item_category: '',
            r_time:''
        }
    },
    actions:{
        [ADD_BEHAVIOR_DATA] ({dispatch, commit, state}, obj) {
            $http.post('/api/behaviors/add', obj).then((data)=>{
                if(data.success){
                    dispatch(GET_BEHAVIOR_DATA)
                    Notification.success('新增成功')
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [DELETE_BEHAVIOR_DATA] ({dispatch, commit, state}, obj) {
            $http.post('/api/behaviors/delete', obj).then((data)=>{
                if(data.success){
                    dispatch(GET_BEHAVIOR_DATA)
                    Notification.success('删除成功')
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [GET_TABLE_DATA]({dispach, commit, state}, obj){
            $http.option('/api/sale/info', state.form).then((data)=>{
                if(data.success){
                    commit(SET_TABLE_DATA, data.data)
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [GET_BEHAVIOR_DATA]({dispach, commit, state}, obj){
            $http.post('/api/behaviors/info').then((data)=>{
                if(data.success){
                    commit(SET_BEHAIVOR_DATA, data.data)
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [DOWNLOAD_CSV_DATA]({dispach, commit, state}, obj){
            $http.option('/api/sale/download').then((data)=>{
                if(data.success){
                    commit(SET_TABLE_DATA, data.data)
                } else {
                    Notification.error('获取失败')
                    
                }
            })
        },
        [GET_CHART_DATA]({dispach, commit, state}, obj){
            $http.option('/api/sale/analysis', state.form).then((data)=>{
                if(data.success){
                    commit(SET_CHART_DATA, data.data)
                } else {
                    Notification.error('获取失败')
                }
            })
        },
        [SUBMIT_FORM_DATA]({dispach, commit, state}, obj){
            $http.post('/api/sale/add', obj).then((data)=>{
                if(data.success){
                    Notification.success('成功')
                    // dispatch(GET_TABLE_DATA)
                } else {
                    Notification.error('失败')
                }
            })
        },
        [GET_PIE_DATA]({dispach, commit, state}, obj){
            $http.get('/api/behaviors/ana').then((data)=>{
                if(data.success){
                    Notification.success('成功')
                    commit(SET_PIE_DATA, data.data)
                } else {
                    Notification.error('失败')
                }
            })
        }
    },
    mutations:{
        [SET_TABLE_DATA](state, data){
            state.tableData = data
        },
        [SET_CHART_DATA](state, data){
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.VALUE)
            })
            state.xdata = temp
            state.ydata = temp1
            state.showFlag = true
        },
        [SET_BEHAIVOR_DATA](state, data){
            state.behaviorData = data
        },
        [SET_PIE_DATA](state, data){
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.num)
            })
            state.piexdata = temp
            state.pieydata = data
            state.showFlag1 = true
        },
    }
}