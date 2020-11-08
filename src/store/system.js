import $http from '../utils/http.js'
import { Notification } from 'element-ui'
import router from '../router/index'
const validcode = 'system/validcode'
const settersLogin = 'system/settersLogin'
const LOG_IN = 'system/LOG_IN'
const settersRoot = 'system/settersRoot'
const auth = 'system/auth'
const logout = 'system/logout'
const changPass = 'system/changePass'
const validationFilling = 'system/validationFilling'
const changeSize = 'system/changeSize'
const SET_MAIN_COUNT = 'system/SET_MAIN_COUNT'
const SET_MENU = 'system/SET_MENU'
const SIGN_IN = 'system/SIGN_IN'
const getPath = function (data) {
    console.log(data, '-=-=-=-')
    if (data.path != undefined && data.path != null) {
        return data.path
    } else {
        return getPath(data.children[0])
    }
}

export default {
    state: {
        mainData: {},
        fixHeadMenu: true,
        fixFooterMenu: true,
        fixLeftMenu: true,
        topicValue: 'blue',
        login: {
            username: '', // 用户名
            password: '', // 密码
            validcodeInput: '', // 用户输入的验证码
            validcode: {
                image: '', // 验证码图片
                originalStr: ''
            }
        },
        changeSizeValue: '',
        showModelChangeInfo: false,
        menu: [], // 改角色拥有的菜单权限
        currentUser: {}, // 当前角色信息,
        showModelChangePass: false,
        changePasswordControlClose: false,
        assetTreeData: [],
        assetTreeDataChoose: [],
        device: [],
        project: {},
        perMsg: [{}],
        editableTabsValue: '/monitor/event',
        editableTabs: [],
        keepAliveInclude: [],
        token: '',
    },
    actions: {
        [LOG_IN]({ dispatch, commit }, obj) {
            debugger
            $http.post('/api/login', obj).then((data) => {
                if (data.data.success) {
                    router.push({name: '地理位置分析'})
                    Notification.success({
                        title: '登录成功'
                    })
                } else {
                    Notification.success('登录失败')
                }
            })
        },
        [logout]({ dispatch, commit }) {
            $http.post('/api/auth/loginout').then(({ status } = {}) => {
                if (status === 'success') {
                    commit(logout)
                }
            })
        },
        [changPass]({ dispatch }, data) {
            $http.post('/api/auth/update', data).then(({ status, msg } = {}) => {
                if (status === 'success') {
                    Notification.success({
                        title: '密码修改成功，请重新登录'
                    })
                    dispatch(logout)
                } else {
                    Notification.warning({
                        title: '密码修改失败',
                        message: msg
                    })
                }
                // commit();
            })
        },
        [SIGN_IN]({ dispatch }, data) {
            $http.post('/api/register', data).then(({ status, msg } = {}) => {
                if (data.data.success) {
                    Notification.success({
                        title: '注册成功'
                    })
                } else {
                    Notification.warning({
                        title: '注册失败',
                        message: msg
                    })
                }
            })
        }
    },
    mutations: {
        [SET_MENU](state, data) {
            if (data.project.name == 'DISPOSAL') {
                data.menu.forEach((item, index) => {
                    if (item.text == '安全门户' || item.text == '信息交换') {
                        data.menu.splice(index, 1)
                    }
                })
            }
            if (data.project.name == 'INFOCHANGE') {
                data.menu.forEach((item, index) => {
                    if (item.text == '数据搜集处理') {
                        data.menu.splice(index, 1)
                    }
                })
            }
            state.menu = data.menu
        },
        [SET_MAIN_COUNT](state, data) {
            state.mainData = data
        },
        [changeSize](state, data) {
            state.changeSizeValue = data
        },
        [logout](state) {
            state.login.username = ''
            state.login.password = ''
            state.login.validcodeInput = ''
        },
        [validcode](state, data) {
            state.login.validcode = {
                image: 'data:image/bmp;base64,' + data.image
            }
            state.login.validcode.originalStr = data.image
        },
        [settersLogin](state, data) {
            state.login[data.key] = data.value
        },
        [settersRoot](state, data) {
            if (data.key === 'currentUser') {
                for (var i in data.value) {
                    if (data.value[i] === null || data.value[i] === '默认节点' || data.value[i] === 'None') {
                        data.value[i] = '-'
                    }
                }
            }
            if (data.key === 'token') {
                document.cookie = 'session' + "=" + escape(data.value) + ";expires=" + new Date((new Date().getTime() + 5 * 60 * 1000));
            }
            if (data.key === 'menu' && data.project === 'PORTAL' && state.currentUser.node_id === 0) {
                const ind = data.value[0].children.findIndex((item, index) => {
                    return item.text === '重保管理'
                })
                data.value[0].children.splice(ind, 1)
            }
            state[data.key] = data.value
            console.log(state)
        },
        [validationFilling](state, data) {
            state.login.validcodeInput = data
        }
    }
}
