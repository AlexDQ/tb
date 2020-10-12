<template>
  <div class='dark'>
    <div class='header'>
      <div class='header-bg'>
      <span class='dateStr'>
          <!-- {{dataStr}} -->
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
          @click='logout'
        >退出登录</el-button>
      </div>
    </div>
    <div class='main-content'>
      <menu>
        <el-menu
          class="el-menu-vertical-demo"
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
        <transition>
            <router-view :key='$route.fullPath'></router-view>
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
import menus from '../components/menus.js'
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
      userModel: false,
      menus:menus,
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
      changePasswordRule: {
        oldPass: [{ validator: checkOldPwd, required: true, trigger: 'blur' }],
        newPass: [{ validator: checkNewPwd, trigger: 'blur', required: true }],
        retPass: [{ validator: checkReNewPwd, trigger: 'blur', required: true }]
      },
      firstTitle: '',
      secendTitle: [],
      sedendIndex: -1,
      Breadcrumb: []
    }
  },
  components: {
  },
  created() {
    // this.getAuth()
    this.Breadcrumb = makeBread(this.$route)
  },
  computed: {
    ...mapState({
      changePasswordControlClose: state =>
        state.system.changePasswordControlClose,
      currentUser: state => state.system.currentUser,
    })
  },
  methods: {
    handleSelect(index, pathIndex) {
      this.getBreadcrumbs(index)
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
    changeFixHead(val) {
      let item = {
        val: val ? 1 : 0
      }
      this.$store.dispatch('system/changeHeadFixed', item)
    },
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
.main-content menu{
  padding: 0;
  width: 196px;
}
.main-content .el-menu{
  background-image: linear-gradient(180deg, #162335 0%, #0D0F1D 100%);
  border-right: none
}
.main-content .el-menu li{
  color: #fff;
}
.el-menu-item:hover{
  background: none !important;
}
.main-content .right_contain{
  background: #EBF1F5;
  overflow-x: hidden;
  /* padding:0 20px 20px 20px; */
}
.main-content .el-menu-item:focus{
  background:#25374F;
  color:#08B6D7
}
.main-content .right_contain .breadcrumb{
  background:#fff;
  padding: 0
}
.main-content .el-submenu__title{
  color: #fff
}
.main-content .el-submenu__title:hover{
  background: none;
}
.header .dateStr{
  font-family: PingFangSC-Regular;
  font-size: 16px;
  color: #FFFFFF;
  line-height: 58px;
  font-weight:lighter;
  position: absolute;
  right: 71px;
}
.header .header-bg{
  height: 56px;
  background-size: cover;
}
</style>








 