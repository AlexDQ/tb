<template>
  <div class='dark'>
    <div class='header'>
      <div class='header-bg'>
      <!-- <i class='icon-antiy'></i> -->
      <!-- <div class='title'>安天战术型态势感知平台</div> -->
      <span class='dateStr'>
          {{dataStr}}
      </span>
      <div class='menu_right'>

        <i
          class='icon-PersonalCenter person'
          @click='userModel=true'
        ></i>
      </div>
    </div>

    </div>

    <div
      class='model_wraper'
      v-show='userModel'
      @click='userModel=false'
    >
      <div class='user'>
        <el-button
          type="primary"
          @click='LOGOUT'
        >退出登录</el-button>
      </div>
    </div>
    <div class='main-content'>
      <!-- <menu>
        <ul>

          <li
           @mouseout="outMenuIndex(index)"
          @click="changeMenuIndex(index)"
            class="menu_li"
            v-for='(item,index) in menus'
            @click='handleMenuClick(item,index,null)'
            :key="index"
            :class="{'active':index==menuIndex }"
          >
            <div class='menu_name'>
              {{item.name}}
              <i
                class='icon-down'
                v-if='item.child'
              ></i>
            </div>
            <div
              class='sub_menu'
              v-if='item.child'
            >
              <ul v-show='index==subMenuIndex && flgI'>
                <li
                  v-for='(k,i) in item.child'
                  :class="{'active_sub':i===subI}"
                  @click='handleMenuClick(k,index,i)'
                  :key="i"
                >
                  {{k.name}}
                </li>
              </ul>
            </div>
          </li>

        </ul>
      </menu> -->
      <menu>
        <!-- background-color="#171E35" -->
        <!-- text-color="rgba(152, 172, 217, 0.7)" -->
        <!-- active-text-color="#FFFFFF" -->
        <el-menu
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          @select="handleSelect"
          active-text-color='#08B6D7'
          :default-active="$route.path"
          :unique-opened='true'
          router
        >
          <div
            v-for='(item,index) in menus'
            :key="index"
          >
            <el-submenu
              v-if='item.children'
              :index="item.group_id"
            >
              <template slot="title">
                <span class="iconBox"><i :class="'icon-'+item.key"></i></span>
                <span>{{item.text}}</span>
              </template>
              <el-menu-item-group>
                <el-menu-item
                  v-for='(k,i) in item.children'
                  :key="i"
                  :index="k.path"
                >{{k.text}}</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item
              v-else
              :index="item.path"
            >
              <span class="iconBox"><i :class="'icon-'+item.key"></i></span>
              <span slot="title">{{item.text}}</span>
            </el-menu-item>
          </div>
        </el-menu>
      </menu>
      <div class='right_contain'>
        <!-- <div class='breadcrumb'>
          <el-breadcrumb separator=">">
            <el-breadcrumb-item
              v-for='(item, index) in breadcrumbs'
              :key='index'
            >{{item}}</el-breadcrumb-item>
          </el-breadcrumb>
        </div> -->
        <transition>
          <!-- <keep-alive max="10"> -->
            <router-view :key='$route.fullPath'></router-view>
            <!-- :closetabs="tabEdit" -->
            <!-- :editableTabs="editableTabs" -->
          <!-- </keep-alive> -->
        </transition>
      </div>
    </div>
    <!-- <el-dialog
      title="修改密码"
      v-model="showModelChangePass"
      :close-on-click-modal="changePasswordControlClose"
      :close-on-press-escape="changePasswordControlClose"
      :show-close="changePasswordControlClose"
      :before-close="close"
      id="changepass"
    >
      <div>
        <el-form
          :model="changePassword"
          :rules="changePasswordRule"
          ref="changePassword"
          label-width="130px"
        >
          <el-form-item
            style="margin-top:0;"
            label="旧密码"
            prop="oldPass"
          >
            <el-input
              v-model="changePassword.oldPass"
              type="password"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="新密码"
            prop="newPass"
          >
            <el-input
              v-model="changePassword.newPass"
              type="password"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="重复新密码"
            prop="retPass"
          >
            <el-input
              v-model="changePassword.retPass"
              type="password"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              style="margin-left:130px;"
              type="primary"
              @click="submitChangePass"
            >确认修改</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog> -->
  </div>
</template>
<script>
import { debounce } from '../utils/debounce.js'
import { compileStr } from '../utils/encryption.js'
import { mapState } from 'vuex'

const matchedType = {
  all: '全部',
  maliciouscode: '恶意代码',
  c2: 'C&C',
  netIntrusion: '网络入侵',
  unfix: '漏洞',
  illegal_access: '违规接入',
  illegal_outer_access: '违规外联',
  attack: '威胁',
  web_threat: '威胁',
  vul: '脆弱性',
  web_visible: '可用性',
  visible: '可用性',
  content: '内容',
  except: '异常'
}

let ansLocationLayout = []
const getMenuListLocation = (name, tree, location) => {
  for (let i = 0; i < tree.length; i++) {
    if (tree[i].text === name) {
      location.push(i)
      ansLocationLayout = location.concat([])
      break
    } else if (tree[i].children !== undefined) {
      let test = location.concat([])
      test.push(i)
      getMenuListLocation(name, tree[i].children, test)
    }
  }
}
const makeBread = data => {
  let ans = []
  for (let i = 0; i < data.matched.length; i++) {
    if (
      data.matched[i].name === undefined ||
      data.matched[i].name == '' ||
      data.matched[i].name.indexOf('@') != -1
    ) {
      continue
    } else {
      ans.push(data.matched[i].name)
    }
  }
  return ans
}
export default {
  data() {
    let checkOldPwd = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('旧密码为必填,请输入旧密码'))
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error('密码长度在 6 到 20 个字符'))
        } else {
          callback()
        }
      }, 1000)
    }
    let checkNewPwd = (rule, value, callback) => {
      var regex = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{6,20}');
      if (value === '') {
        callback(new Error('请输入密码'))
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error('密码长度在 6 到 20 个字符'))
        } else if (!regex.test(value)) {
          callback(new Error('您的密码复杂度太低,密码中必须包含大小写字母、数字、特殊字符'))
        } else {
          if (value === this.changePassword.oldPass) {
            callback(new Error('新密码与旧密码不能相同'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
    let checkReNewPwd = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error('密码长度在 6 到 20 个字符'))
        } else {
          if (value !== this.changePassword.newPass) {
            callback(new Error('两次输入的密码不一致'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
    return {
      dialogVisibleOne: false,
      setTingTopic: false,
      changeTopic: false,
      tabIndex: 1,
      lineIndex: 0,
      showListSwitch: false,
      showTypeLayout: true,
      title: '通报预警子系统',
      showKind: true,
      showControl: -1,
      showControlExpand: -1,
      showControlChild: -1,
      showControlChangeAsset: false,
      changePassword: {
        oldPass: '',
        newPass: '',
        retPass: ''
      },
      menus:[],
      changePasswordRule: {
        oldPass: [{ validator: checkOldPwd, required: true, trigger: 'blur' }],
        newPass: [{ validator: checkNewPwd, trigger: 'blur', required: true }],
        retPass: [{ validator: checkReNewPwd, trigger: 'blur', required: true }]
      },
      filterText: '',
      defaultProps: {
        children: 'children',
        label: 'label'
      },

      locationStyle: {
        width: 200 + 'px',
        top: 89 + 'px',
        left: 50 + 'px',
        display: 'block'
      },
      firstTitle: '',
      secendTitle: [],
      sedendIndex: -1,
      Breadcrumb: []
    }
  },
  mounted() {
    // this.$store.dispatch('system/getTheme')
  },
  watch: {
    // filterText (val) {
    //   this.$refs.tree.filter(val)
    // },
    assetTreeDataChoose(value) {
      // this.$refs.tree.setCheckedKeys(value)
    },
    $route(to) {
      let name = this.$route.name
      if (
        this.$route.name === undefined ||
        this.$route.name === '' ||
        this.$route.name.indexOf('@') != -1
      ) {
        for (let i in this.$route.matched) {
          if (
            this.$route.matched[i].name === undefined ||
            this.$route.matched[i].name === '' ||
            this.$route.name.indexOf('@') != -1
          ) {
            if (i != 0) {
              name = this.$route.matched[i - 1].name
            } else {
              name = ''
            }
          }
        }
      }
      if (name === '监测日志') {
        name = matchedType[to.params.id]
      }
      ansLocationLayout = []
      getMenuListLocation(name, this.menu, [])
      if (ansLocationLayout.length === 0) {
        for (let i in this.$route.matched) {
          if (this.$route.matched[i].name === name) {
            name = this.$route.matched[i - 1].name
            getMenuListLocation(name, this.menu, [])
            if (ansLocationLayout.length === 1) {
              this.lineIndex = ansLocationLayout[0]
            } else if (ansLocationLayout.length === 2) {
              this.lineIndex = ansLocationLayout[0]
              this.showControl = ansLocationLayout[1]
              this.showControlExpand = ansLocationLayout[1]
            } else {
              this.lineIndex = ansLocationLayout[0]
              this.showControl = ansLocationLayout[1]
              this.showControlExpand = ansLocationLayout[1]
              this.showControlChild = ansLocationLayout[2]
            }
          }
        }
      } else if (ansLocationLayout.length === 1) {
        this.lineIndex = ansLocationLayout[0]
      } else if (ansLocationLayout.length === 2) {
        this.lineIndex = ansLocationLayout[0]
        this.showControl = ansLocationLayout[1]
        this.showControlExpand = ansLocationLayout[1]
      } else {
        this.lineIndex = ansLocationLayout[0]
        this.showControl = ansLocationLayout[1]
        this.showControlExpand = ansLocationLayout[1]
        this.showControlChild = ansLocationLayout[2]
      }
      this.Breadcrumb = makeBread(this.$route)
    },
    menu() {
      let name = this.$route.name
      if (
        this.$route.name === undefined ||
        this.$route.name === '' ||
        this.$route.name.indexOf('@') != -1
      ) {
        for (let i in this.$route.matched) {
          if (
            this.$route.matched[i].name === undefined ||
            this.$route.matched[i].name === '' ||
            this.$route.name.indexOf('@') != -1
          ) {
            if (i != 0) {
              name = this.$route.matched[i - 1].name
            } else {
              name = ''
            }
          }
        }
      }
      if (name === '监测日志') {
        name = matchedType[this.$route.params.id]
      }
      ansLocationLayout = []
      getMenuListLocation(name, this.menu, [])
      if (ansLocationLayout.length === 0) {
        for (let i in this.$route.matched) {
          if (this.$route.matched[i].name === name) {
            name = this.$route.matched[i - 1].name
            getMenuListLocation(name, this.menu, [])
            this.lineIndex = ansLocationLayout[0]
          }
        }
      } else if (ansLocationLayout.length === 1) {
        this.lineIndex = ansLocationLayout[0]
      } else if (ansLocationLayout.length === 2) {
        this.lineIndex = ansLocationLayout[0]
        this.showControl = ansLocationLayout[1]
        this.showControlExpand = ansLocationLayout[1]
      } else {
        this.lineIndex = ansLocationLayout[0]
        this.showControl = ansLocationLayout[1]
        this.showControlExpand = ansLocationLayout[1]
        this.showControlChild = ansLocationLayout[2]
      }
      this.Breadcrumb = makeBread(this.$route)
    }
    // for (let i = 0; i < currentUser.length; i++) {

    // }
  },
  components: {
  },
  created() {
    this.getAuth()
    this.Breadcrumb = makeBread(this.$route)
  },
  computed: {
    ...mapState({
      changePasswordControlClose: state =>
        state.system.changePasswordControlClose,
      menu: state => state.system.menu,
      currentUser: state => state.system.currentUser,
      assetTreeData: state => state.system.assetTreeData,
      assetTreeDataChoose: state => state.system.assetTreeDataChoose
    }),
    showModelChangePass: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'showModelChangePass',
          value: val
        })
      },
      get() {
        return this.$store.state.system.showModelChangePass
      }
    },
    showModelChangeInfo: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'showModelChangeInfo',
          value: val
        })
      },
      get() {
        return this.$store.state.system.showModelChangeInfo
      }
    },
    fixHeadMenu: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'fixHeadMenu',
          value: val
        })
      },
      get() {
        return this.$store.state.system.fixHeadMenu
      }
    },
    fixFooterMenu: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'fixFooterMenu',
          value: val
        })
      },
      get() {
        return this.$store.state.system.fixFooterMenu
      }
    },
    fixLeftMenu: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'fixLeftMenu',
          value: val
        })
      },
      get() {
        return this.$store.state.system.fixLeftMenu
      }
    },
    topicValue: {
      set(val) {
        this.$store.commit('system/settersRoot', {
          key: 'topicValue',
          value: val
        })
      },
      get() {
        return this.$store.state.system.topicValue
      }
    }
  },
  methods: {
    returnMain() {
      this.$router.push({ path: '/main' })
    },
    changeColor(val) {
      let item = {
        val: val
      }
      this.$store.dispatch('system/changeTheme', item)
    },
    changeShowType() {
      this.showTypeLayout = !this.showTypeLayout
      this.$store.commit('system/changeSize', this.showTypeLayout)
    },
    checkChosseKey() {
      this.showControlChangeAsset = false
      this.$store.dispatch(
        'system/changeFollowAsset',
        this.$refs.tree.getCheckedKeys()
      )
    },
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    changeShowModelChangeAsset() {
      this.filterText = ''
      this.getAssetFollow()
      this.showControlChangeAsset = true
    },
    getAssetFollow() {
      this.$store.dispatch('system/getAssetFollow')
      this.$store.dispatch('system/getFollowAsset')
    },
    close() {
      this.$refs['changePassword'].resetFields()
      this.$store.commit('system/settersRoot', {
        key: 'showModelChangePass',
        value: false
      })
    },
    changeShowModelChangeInfo() {
      this.dialogVisibleOne = true
    },
    cancel() {
      this.dialogVisibleOne = false
    },
    changeShowModelChangePass() {
      this.$store.commit('system/settersRoot', {
        value: true,
        key: 'changePasswordControlClose'
      })
      this.$store.commit('system/settersRoot', {
        key: 'showModelChangePass',
        value: true
      })
    },
    getAuth() {
      this.$store.dispatch('system/auth')
    },
    secendJump(url) {
      console.log(url)
      this.showControl = this.sedendIndex
      this.jumpAll(url)
    },
    mouseoverList(index) {
      if (!this.showTypeLayout) {
        this.sedendIndex = index
        this.firstTitle = this.menu[this.lineIndex].children[index].text
        this.secendTitle = this.menu[this.lineIndex].children[index].children
        this.locationStyle = {
          width: 180 + 'px',
          top: 40 + index * 40 + 'px',
          left: 40 + 'px',
          display: 'block',
          'z-index': 1000
        }
        this.showListSwitch = true
      }
    },
    jumpAll(url) {
      if (url !== null || url !== undefined) {
        // this.$store.dispatch('system/jumpUrl', url)
        this.$router.push(url)
      }
    },
    changeMenu(index, list) {
      var children = list.children
      if (children === undefined) {
        window.open('/view')
      } else if (children[0].path) {
        this.jumpAll(children[0].path)
        this.lineIndex = index
      } else {
        this.jumpAll(children[0].children[0].path)
        this.lineIndex = index
      }

      // this.jumpAll(url)
    },
    /*******/
    changeFixHead(val) {
      let item = {
        val: val ? 1 : 0
      }
      this.$store.dispatch('system/changeHeadFixed', item)
    },
    changeLeftMenu(val) {
      let item = {
        val: val ? 1 : 0
      }
      this.$store.dispatch('system/changeLeftMenu', item)
    },
    changeFixFooter(val) {
      let item = {
        val: val ? 1 : 0
      }
      this.$store.dispatch('system/changeFooterFixed', item)
    },
    changeControler: debounce(
      function(type, index, url) {
        if (type === 'parent') {
          this.menu[this.lineIndex].children[index].expand = !this.menu[
            this.lineIndex
          ].children[index].expand
          if (url) {
            this.jumpAll(url)
          }
        } else if (type === 'child') {
          this.jumpAll(url)
        }
      },
      500,
      true
    ),
    logout() {
      this.$store.dispatch('system/logout')
    },
    changePassShow() {
      this.showModelChangePass = true
    },
    submitChangePass() {
      this.$refs['changePassword'].validate(valid => {
        if (valid) {
          let changeData = {
            oldPwd: compileStr(this.changePassword.oldPass),
            newPwd: compileStr(this.changePassword.newPass),
            retPwd: compileStr(this.changePassword.retPass)
          }
          this.$store.dispatch('system/changePass', changeData)
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style>
/*.main-tabs {
  border-bottom: 1px solid #d3dce8;
}*/
.chose-topic .el-radio .is-checked + span {
  color: #5c6781;
}
.main-tabs .el-tabs--card > .el-tabs__header .el-tabs__item {
  border-bottom: 1px solid #d3dce8;
  background: transparent;
}
.main-tabs .el-tabs--card {
  position: relative !important;
  margin-left: 0 !important;
}
.main-tabs .el-tabs__header {
  border: 0;
  margin: 0;
  /* margin-left:-20px;
  margin-right:-20px; */
  width: 100%;
}
.main-tabs .el-tabs--card > .el-tabs__header .el-tabs__item {
  border-top: 0;
  border-left: 0;
  border-right: 0;
}
.main-tabs .el-tabs__item {
  position: relative;
  display: inline-block;
  z-index: 0;
  background: transparent;
  height: 29px;
  line-height: 29px;
  border-bottom: 1px solid #d3dce8;
}

.main-tabs .header-tabs .el-tabs__nav-scroll {
  background: #f7f8fa;
  padding-left: 20px;
  padding-top: 2px;
}

.main-tabs .el-tabs__item.is-active {
  color: #5c6781;
}

.main-tabs .el-tabs__nav {
  border: 0;
}
.main-tabs .el-tabs--card > .el-tabs__header .el-tabs__nav {
  border-bottom: 0;
  padding: 0;
}
.main-tabs .el-tabs--card > .el-tabs__header .el-tabs__item {
  margin-left: 0px;
  min-width: 100px;
}
.main-tabs .el-tabs--card > .el-tabs__header .el-tabs__item.is-active {
  border-top: 0;
  border-left: 0;
  border-right: 0;
}

.main-tabs .el-tabs__header .el-tabs__nav > .el-tabs__item::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: -1;
  background-image: linear-gradient(
    hsla(0, 0%, 100%, 0.6),
    hsla(0, 0%, 100%, 0)
  );
  border: 1px solid #d3dce8;
  border-bottom: none;
  box-shadow: 0 0.15em #ffffff inset;
  transform: perspective(0.3em) rotateX(1deg);
  transform-origin: bottom;
}
.main-tabs .el-tabs__nav > .el-tabs__item.is-active::before {
  background: #ecf0f5;
  box-shadow: 0 0.15em #ecf0f5 inset;
}
/* .main-tabs .el-tabs__nav-wrap{
  padding-left:20px;
} */
.el-tabs--card > .el-tabs__header .el-tabs__item.is-active.is-closable {
  z-index: 1;
}
#main-contain .el-tabs__header .el-tabs__nav > .el-tabs__item::before {
  content: '';
  position: static;
  z-index: 0;
  background-image: '';
  border: 0;
  border-bottom: none;
  box-shadow: 0;
  transform: 0;
  transform-origin: bottom;
}
.el-tabs__content {
  border-top: 1px solid #d3dce8;
}
#main-contain .el-tabs__content {
  border-top: 0;
}
/* .el-dialog-box .el-dialog--tiny .el-dialog__header {
  padding: 0 20px;
  height: 40px;
  line-height: 38px;
  border: 1px solid #1f92ef;
  background-color: #1f92ef;
}
.el-dialog-box .el-dialog--tiny .el-dialog__title {
  color: #ffffff;
  font-size: 14px;
  font-weight: 400;
} */
/* .el-dialog-box .el-dialog--tiny {
    width: 500px;
    height: 455px;
    border: 1px solid #e3e9ec;
} */
.titlename {
  width: 80px;
  height: 40px;

  padding-right: 15px;
  text-align: right;
  font-size: 12px;
}
.titledata {
  word-wrap: break-word;
  width: 200px;
  height: 40px;
  font-size: 12px;

  padding-left: 15px;
}
.per_massage_dialog .el-dialog__body {
  padding: 20px !important;
}
.per_massage {
  border: 1px solid #eeeeee;
}
.el-tab-pane #bread-title {
  padding: 12px;
  padding-left: 20px;
  /* border: 1px solid #eeeeee; */
  border-top: 0;
  background: transparent;
  /* margin-bottom: 20px; */
}
#eldialog .el-dialog__body {
  padding: 0 !important;
  color: #5c6781;
  font-size: 14px;
  min-height: 100px;
  border-bottom: 1px solid #eee;
}
/* #bread-title .el-breadcrumb{
  height:40px;
  line-height:40px;
} */
</style>








 