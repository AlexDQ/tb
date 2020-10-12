<template>
  <div class="dark">
    <div class="header">
      <h3 style="color: #fff; opacity: 0.8; line-height: 40px; margin-top: 0">
        基于淘宝用户行为分析可视化平台
      </h3>
      <!-- <span style='position: absolute;top: 0;right: 0;'>用户</span> -->
      <el-dropdown style="position: absolute; top: 0; right: 0">
        <el-button type="primary">
          用户<i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native='showEditInfoDialog'>个人信息修改</el-dropdown-item>
          <el-dropdown-item @click.native='changePassShow'>修改密码</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <div style="clear: both"></div>
    </div>
    <div class="main-content">
      <menu>
        <el-menu
          class="el-menu-vertical-demo"
          @select="handleSelect"
          active-text-color="#08B6D7"
          :default-active="$route.path"
          :unique-opened="true"
          router
        >
          <div v-for="(item, index) in menus" :key="index">
            <el-submenu v-if="item.children" :index="item.group_id">
              <template slot="title">
                <span class="iconBox"><i :class="'icon-' + item.key"></i></span>
                <span>{{ item.text }}</span>
              </template>
              <el-menu-item-group>
                <el-menu-item
                  v-for="(k, i) in item.children"
                  :key="i"
                  :index="k.path"
                  >{{ k.text }}</el-menu-item
                >
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item v-else :index="item.path">
              <span class="iconBox"><i :class="'icon-' + item.key"></i></span>
              <span slot="title">{{ item.text }}</span>
            </el-menu-item>
          </div>
        </el-menu>
      </menu>
      <div class="right_contain">
        <transition>
          <router-view :key="$route.fullPath"></router-view>
        </transition>
      </div>
    </div>
    <el-dialog
      title="个人信息修改"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="close"
    >
      <el-form ref="signUpForm" :model="signUpForm" :rules="rule">
        <el-form-item prop="name" label="姓名">
          <el-input v-model="signUpForm.name"></el-input>
        </el-form-item>
        <el-form-item prop="email" label="邮箱">
          <el-input v-model="signUpForm.name"></el-input>
        </el-form-item>
        <el-form-item prop="tel" label="电话">
          <el-input v-model="signUpForm.tel"></el-input>
        </el-form-item>
        <el-form-item prop="sex" label="性别">
          <el-select v-model="signUpForm.sex">
            <el-option label="男" value="1"></el-option>
            <el-option label="女" value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="age" label="年龄">
          <el-input v-model="signUpForm.age"></el-input>
        </el-form-item>
        <el-form-item prop="address" label="家庭住址">
          <el-input v-model="signUpForm.address"></el-input>
        </el-form-item>
      </el-form>
	  <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <el-dialog
      title="修改密码"
      :visible.sync="showModelChangePass"
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
    </el-dialog>
  </div>
</template>
<script>
import { debounce } from "../utils/debounce.js";
import { compileStr } from "../utils/encryption.js";
import { mapState } from "vuex";
import menus from "../components/menus.js";
let ansLocationLayout = [];
const getMenuListLocation = (name, tree, location) => {
  for (let i = 0; i < tree.length; i++) {
    if (tree[i].text === name) {
      location.push(i);
      ansLocationLayout = location.concat([]);
      break;
    } else if (tree[i].children !== undefined) {
      let test = location.concat([]);
      test.push(i);
      getMenuListLocation(name, tree[i].children, test);
    }
  }
};
const makeBread = (data) => {
  let ans = [];
  for (let i = 0; i < data.matched.length; i++) {
    if (
      data.matched[i].name === undefined ||
      data.matched[i].name == "" ||
      data.matched[i].name.indexOf("@") != -1
    ) {
      continue;
    } else {
      ans.push(data.matched[i].name);
    }
  }
  return ans;
};
export default {
  data() {
	let checkName = (rule, value, callback) => {
      if (value === "" || value === null) {
        callback(new Error("请输入姓名"));
      } else {
        callback();
      }
    };
    let checkTel = (rule, value, callback) => {
      var regex = new RegExp("/^1[3456789]d{9}$/");
      if (!regex.test(value)) {
        callback(new Error("请输入正确格式的手机号码"));
      } else {
        callback();
      }
    };
    let checkEmail = (rule, value, callback) => {
      var regex = new RegExp("/^([a-zA-Zd])(w|-)+@[a-zA-Zd]+.[a-zA-Z]{2,4}$/");
      if (!regex.test(value)) {
        callback(new Error("请输入正确格式的电子邮箱"));
      } else {
        callback();
      }
    };
    let checkOldPwd = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("旧密码为必填,请输入旧密码"));
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error("密码长度在 6 到 20 个字符"));
        } else {
          callback();
        }
      }, 1000);
    };
    let checkNewPwd = (rule, value, callback) => {
      var regex = new RegExp(
        "(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{6,20}"
      );
      if (value === "") {
        callback(new Error("请输入密码"));
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error("密码长度在 6 到 20 个字符"));
        } else if (!regex.test(value)) {
          callback(
            new Error(
              "您的密码复杂度太低,密码中必须包含大小写字母、数字、特殊字符"
            )
          );
        } else {
          if (value === this.changePassword.oldPass) {
            callback(new Error("新密码与旧密码不能相同"));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    let checkReNewPwd = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      }
      setTimeout(() => {
        if (String(value).length > 20 || String(value).length < 6) {
          callback(new Error("密码长度在 6 到 20 个字符"));
        } else {
          if (value !== this.changePassword.newPass) {
            callback(new Error("两次输入的密码不一致"));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    return {
      dialogVisible: false,
      menus: menus,
      signUpForm: {
        tel: "",
        email: "",
        address: "",
        age: "",
        sex: "",
        name: "",
      },
      rule: {
        name: [{ validator: checkName, required: true, trigger: "blur" }],
        email: [{ validator: checkEmail, required: true, trigger: "blur" }],
        tel: [{ validator: checkTel, required: true, trigger: "blur" }],
      },
      changePassword: {
        oldPass: "",
        newPass: "",
        retPass: "",
      },
      changePasswordRule: {
        oldPass: [{ validator: checkOldPwd, required: true, trigger: "blur" }],
        newPass: [{ validator: checkNewPwd, trigger: "blur", required: true }],
        retPass: [
          { validator: checkReNewPwd, trigger: "blur", required: true },
        ],
      },
      Breadcrumb: [],
    };
  },
  components: {},
  created() {
    // this.getAuth()
    this.Breadcrumb = makeBread(this.$route);
  },
  computed: {
    ...mapState({
      changePasswordControlClose: (state) =>
        state.system.changePasswordControlClose,
	  currentUser: (state) => state.system.currentUser,
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
  },
  methods: {
	showEditInfoDialog () {
		this.dialogVisible = true
	},
    handleSelect(index, pathIndex) {
      this.getBreadcrumbs(index);
	},
	close1 () {
		this.dialogVisible = false
	},
    close() {
      this.$refs["changePassword"].resetFields();
      this.$store.commit("system/settersRoot", {
        key: "showModelChangePass",
        value: false,
      });
    },
    changeShowModelChangePass() {
      this.$store.commit("system/settersRoot", {
        value: true,
        key: "changePasswordControlClose",
      });
      this.$store.commit("system/settersRoot", {
        key: "showModelChangePass",
        value: true,
      });
    },
    getAuth() {
      this.$store.dispatch("system/auth");
    },
    changeFixHead(val) {
      let item = {
        val: val ? 1 : 0,
      };
      this.$store.dispatch("system/changeHeadFixed", item);
    },
    logout() {
      this.$store.dispatch("system/logout");
	},
	submitForm (formName) {
      this.$refs['singUpForm'].validate((valid) => {
        if (valid) {
            // this.$store.dispatch('otherk/editdata', this.signUpForm)
        } else {
          return false;
        }
      })
	},
    changePassShow() {
      this.showModelChangePass = true;
    },
    submitChangePass() {
      this.$refs["changePassword"].validate((valid) => {
        if (valid) {
          let changeData = {
            oldPwd: compileStr(this.changePassword.oldPass),
            newPwd: compileStr(this.changePassword.newPass),
            retPwd: compileStr(this.changePassword.retPass),
          };
          this.$store.dispatch("system/changePass", changeData);
        } else {
          return false;
        }
      });
    },
  },
};
</script>
<style>
.dark {
  height: calc(100% - 40px);
}
.main-content {
  height: 100%;
  width: 100%;
  display: flex;
}
.main-content menu {
  padding: 0;
  margin-top: 0;
  /* height:100%; */
  width: 220px;
  min-width: 220px;
  height: 100%;
  margin: 0;
  padding: 0;
  font-size: 14px;
}
.main-content .el-menu {
  background-image: linear-gradient(180deg, #162335 0%, #0d0f1d 100%);
  border-right: none;
  height: 100%;
}
.main-content .el-menu li {
  color: #fff;
}
.el-menu-item:hover {
  background: none !important;
}
.main-content .right_contain {
  background: #ebf1f5;
  overflow-x: hidden;
  flex: 1;
  /* padding:0 20px 20px 20px; */
}
.main-content .el-menu-item:focus {
  background: #25374f;
  color: #08b6d7;
}
.main-content .right_contain .breadcrumb {
  background: #fff;
  padding: 0;
}
.main-content .el-submenu__title {
  color: #fff;
}
.main-content .el-submenu__title:hover {
  background: none;
}
.header {
  width: 100%;
  background-image: linear-gradient(180deg, #162335 0%, #0d0f1d 100%);
  height: 40px;
}
</style>








 