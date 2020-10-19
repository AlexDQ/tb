import $http from '../utils/http.js'
import { Notification } from 'element-ui'
import router from '../router/index'
const validcode = 'system/validcode'
const settersLogin = 'system/settersLogin'
const login = 'system/login'
const settersRoot = 'system/settersRoot'
const auth = 'system/auth'
const logout = 'system/logout'
const changPass = 'system/changePass'
const validationFilling = 'system/validationFilling'
const changeSize = 'system/changeSize'
const SET_MAIN_COUNT = 'system/SET_MAIN_COUNT'
const SET_MENU = 'system/SET_MENU'
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
        [validcode]({ commit }) {
            $http.get('/api/validcode').then(({ status, msg, data } = {}) => {
                if (status === 'success') commit(validcode, data)
                else {
                    Notification.error({
                        title: '验证码获取失败',
                        message: msg
                    })
                }
            })
        },
        [login]({ dispatch, commit, state }, value) {
            commit(settersRoot, { value: '', key: 'editableTabsValue' })
            commit(settersRoot, { value: [], key: 'editableTabs' })
            commit(settersRoot, { value: [], key: 'keepAliveInclude' })
            $http.post('/api/auth', value).then(({ status, msg, data } = {}) => {
                if (status === 'success') {
                    Notification.success('登录成功')
                    state.login = {
                        username: '', // 用户名
                        password: '', // 密码
                        validcodeInput: '', // 用户输入的验证码
                        validcode: {
                            image: '' // 验证码图片
                        }
                    }
                    let menu = []
                    data.menu.map(vals => {
                        if (vals.key.toUpperCase() === data.project.name) {
                            menu.push(vals)
                        }
                    })
                    console.log(JSON.parse(JSON.stringify(menu)))
                    // commit(settersRoot, {value: menus, key: 'menu'})
                    commit(settersRoot, { value: data.user, key: 'currentUser' })
                    commit(settersRoot, { value: data.menu, key: 'menu', project: data.project.name })
                    commit(settersRoot, { value: data.token, key: 'token' })
                    console.log(data.project.name)
                    let a = new Date() - new Date(data.user.update_time).getTime()
                    console.log(a)
                    if (a > 57 * 24 * 60 * 60 * 1000) {
                        Notification.info('请及时修改密码')
                    }
                    if (data.project.name) {
                        localStorage.setItem("project", JSON.stringify(data.project.name))
                    }
                    // router.push(getPath(menu[0]))

                    // router.push('/web/warnings/validate')
                    // if (data.user.role_id === 1) router.push('/system/users')
                    // else if (data.user.role_id === 2) router.push('/test')
                    // else if (data.user.role_id === 3) router.push('/logger')
                } else {
                    Notification.error({
                        title: '登录失败',
                        message: msg
                    })
                    dispatch(validcode)
                }
            })
        },
        async [auth]({ dispatch, commit }) {
            let result = await $http.get('/api/auth')
            if (result) {
                let { status, data } = result
                if (status === 'success') {
                    for (let i in data.menu) {
                        for (let j in data.menu[i].children) {
                            this._vm.$set(data.menu[i].children[j], 'expand', false)
                        }
                    }
                    let menu = []
                    data.menu.map(vals => {
                        if (vals.key.toUpperCase() === data.project.name) {
                            menu.push(vals)
                        }
                    })
                    for (let i in data.menu) {
                        for (let j in data.menu[i].children) {
                            this._vm.$set(data.menu[i].children[j], 'expand', false)
                        }
                    }
                    commit(settersRoot, { value: data.token, key: 'token' })
                    // commit(settersRoot, {value: menus, key: 'menu'})
                    // commit(settersRoot, { value: data.menu, key: 'menu' })
                    // commit(settersRoot, { value: { ...data.user }, key: 'currentUser' })
                    commit(settersRoot, { value: data.menu, key: 'menu', project: data.project.name })
                    commit(SET_MENU, data)
                    commit(settersRoot, { value: false, key: 'showModelChangePass' })
                    // commit(settersRoot, { value: data.menu, key: 'menu' })
                    commit(settersRoot, { value: data.device, key: 'device' })
                    commit(settersRoot, { value: data.project, key: 'project' })
                } else if (status === 'default') {
                    commit(settersRoot, { value: false, key: 'changePasswordControlClose' })
                    commit(settersRoot, { value: true, key: 'showModelChangePass' })
                    Notification.warning({
                        title: '请修改初始密码'
                        // message:msg
                    })
                } else {
                    // Notification.warning({
                    //     title:"没有权限，或权限已经失效",
                    //     message:msg
                    // })
                    dispatch(logout)
                    router.push('/login')
                }
            }
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
