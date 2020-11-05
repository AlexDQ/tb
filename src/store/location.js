import $http from '../utils/http.js'
import { Notification } from 'element-ui'
import router from '../router/index'
const GET_CHART_DATA = 'location/GET_CHART_DATA'
const SET_CHART_DATA = 'location/SET_CHART_DATA'
const GET_PV_DATA = 'location/GET_PV_DATA'
const SET_PV_DATA = 'location/SET_PV_DATA'
const GET_UV_DATA = 'location/GET_UV_DATA'
const SET_UV_DATA = 'location/SET_UV_DATA'
const GET_TOTAL_DATA = 'location/GET_TOTAL_DATA'
const SET_TOTAL_DATA = 'location/SET_TOTAL_DATA'
const GET_BUY_DATA = 'location/GET_BUY_DATA'
const SET_BUY_DATA = 'location/SET_BUY_DATA'
const GET_TIME_DATA = 'location/GET_TIME_DATA'
const SET_TIME_DATA = 'location/SET_TIME_DATA'

export default {
    state: {
        location_data: {},
        showFlag: false,
        showFlag1: false,
        showFlag2: false,
        showFlag3: false,
        showFlag4: false,
        pvdata:{},
        pvXdata:[],
        pvYdata:[],
        uvXdata:[],
        uvYdata:[],
        totalXdata:[],
        totalYdata:[],
        buyXdata: [],
        buyXdata:[],
        buyData: []
    },
    actions: {
        [GET_CHART_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/country', obj).then((data) => {
                if (data.success) {
                    commit(SET_CHART_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
        [GET_PV_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/pv', obj).then((data) => {
                if (data.success) {
                    commit(SET_PV_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
        [GET_UV_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/uv', obj).then((data) => {
                if (data.success) {
                    commit(SET_UV_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
        [GET_TOTAL_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/total', obj).then((data) => {
                if (data.success) {
                    commit(SET_TOTAL_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
        [GET_BUY_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/xg', obj).then((data) => {
                if (data.success) {
                    commit(SET_BUY_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
        [GET_TIME_DATA]({ dispatch, commit }, obj) {
            $http.post('/api/analysis/sj', obj).then((data) => {
                if (data.success) {
                    commit(SET_TIME_DATA, data.data)
                } else {
                    Notification.success('获取失败')
                }
            })
        },
    },
    mutations: {
        [SET_CHART_DATA](state, data){
            data.forEach((item, index)=>{
                state.location_data[item.name] = item.VALUE
            })
            console.log(state.location_data)
            state.showFlag = true
        },
        [SET_PV_DATA](state, data){
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.VALUE)
            })
            state.pvXdata = temp
            state.pvYdata = temp1
            state.showFlag1 = true
        },
        [SET_UV_DATA](state, data){
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.VALUE)
            })
            state.uvXdata = temp
            state.uvYdata = temp1
            state.showFlag2 = true
        },
        [SET_TOTAL_DATA](state, data){
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.VALUE)
            })
            state.totalXdata = temp
            state.totalYdata = temp1
            state.showFlag3 = true
        },
        [SET_TIME_DATA](){
            // let temp = [], temp1 = []
            // data.forEach((item, index)=>{
            //     temp.push(item.name)
            //     temp1.push(item.VALUE)
            // })
            // state.totalXdata = temp
            // state.totalYdata = temp1
            // state.showFlag3 = true
        },
        [SET_BUY_DATA](state, data){
            state.buyData = data
            let total
            if(data.length > 1){
                total = data.forEach((a, b)=>{
                    return Number(a.value) + Number(b.value)
                })
            } else {
                total = data[0].value
            }
            
            state.buyData.forEach((item, index)=>{
                item.value = item.value / total * 100
            })
            let temp = [], temp1 = []
            data.forEach((item, index)=>{
                temp.push(item.name)
                temp1.push(item.value)
            })
            state.buyXdata = temp
            state.buyYdata = temp1
            state.showFlag4 = true
        },
    }
}
