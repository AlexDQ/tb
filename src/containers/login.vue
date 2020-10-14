<template>
  <div id="container" class="cls-container">
    <div class="cls-content">
      <div class="cls-content-sm panel">
        <div class="panel-body">
          <div class="mar-ver pad-btm">
            <div style="margin-top: 135px"></div>
            <!-- <i class='saas-icon-antiy' style="font-size:65px;color:#455b6b"/> -->
            <h3 style="color: #455b6b; font-size: 18px">
              基于淘宝用户行为分析可视化平台
            </h3>
          </div>
          <form v-on:submit.prevent="submit">
            <div class="form-group">
              <div class="input-group">
                <el-input
                  style="
                    border-top-right-radius: 20px;
                    border-bottom-right-radius: 20px;
                  "
                  type="text"
                  class="form-control"
                  placeholder="账号"
                  v-model="username"
                  @input="changeValue('username', $event.target.value)"
                />
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <el-input
                  style="
                    border-top-right-radius: 20px;
                    border-bottom-right-radius: 20px;
                  "
                  type="password"
                  class="form-control"
                  placeholder="密码"
                  @input="changeValue('password', $event.target.value)"
                  v-model="password"
                />
              </div>
            </div>
            <div class="form-group" style="margin-bottom: 21px">
              <div class="input-group">
                <el-input
                  autocomplete="off"
                  type="text"
                  class="form-control"
                  placeholder="验证码"
                  id="va"
                  @input="changeValue('validcodeInput', $event.target.value)"
                  v-model="validcodeInput"
                />
                <img
                  style="
                    border-top-right-radius: 20px;
                    border-bottom-right-radius: 20px;
                  "
                  v-bind:src="validcode.image"
                  id="vaImg"
                  v-on:click="getValidcode"
                />
              </div>
              <div class="clearFloat"></div>
            </div>
            <div class="form-group">
              <el-button type="primary" @click="submit" id="loginButton"
                >登 录</el-button
              >
            </div>
          </form>
          <div class="form-group">
            <el-button type="primary" @click="showSignUpDialog" id="loginButton"
              >注册</el-button
            >
          </div>
		      <div class="form-group">
            <el-button type="primary" @click="showForgetDialog" id="loginButton"
              >忘记密码</el-button
            >
          </div>
        </div>
      </div>
    </div>
	<el-dialog
      title="提示"
      :visible.sync="dialogVisible1"
      width="30%"
      :before-close="handleClose1"
    >
      <span>这是一段信息</span>
      <el-form ref='forgetForm' :model="forgetForm" :rules="rule1">
        <el-form-item prop="email" label="邮箱">
          <el-input v-model="forgetForm.name"></el-input>
        </el-form-item>
        <el-form-item prop="passwd" label="密码">
          <el-input v-model="forgetForm.passwd"></el-input>
        </el-form-item>
		<el-form-item prop="repeatPasswd" label="确认密码">
          <el-input v-model="forgetForm.repeatPasswd"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm1"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <el-dialog
      title="注册"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form ref='signUpForm' :model="signUpForm" :rules="rule">
        <el-form-item prop="name" label="姓名">
          <el-input v-model="signUpForm.name"></el-input>
        </el-form-item>
        <el-form-item prop="email" label="邮箱">
          <el-input v-model="signUpForm.name"></el-input>
        </el-form-item>
        <el-form-item prop="passwd" label="密码">
          <el-input v-model="signUpForm.passwd"></el-input>
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
  </div>
</template>
<script>
import { compileStr } from "../utils/encryption.js";
import { debounce } from "../utils/debounce.js";
import { Notification } from "element-ui";
export default {
  data() {
    let checkName = (rule, value, callback) => {
      if (value === "" || value === null) {
        callback(new Error("请输入姓名"));
      } else {
        callback();
      }
    };
    let checkPWD = (rule, value, callback) => {
      if (value === "" || value === null) {
        callback(new Error("请输入密码"));
      } else {
        if (value.length < 6) {
          callback(new Error("密码长度不能小于6位"));
        }
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
    return {
	  dialogVisible1: false,
	  dialogVisible: false,
	  forgetForm:{
		email: '',
		passwd: '',
		repeatPasswd: ''
	  },
    signUpForm: {
      tel: "",
      email: "",
      address: "",
      age: "",
      sex: "",
      passwd: "",
      name: "",
    },
    rule: {
      name: [{ validator: checkName, required: true, trigger: "blur" }],
      passwd: [{ validator: checkPWD, required: true, trigger: "blur" }],
      email: [{ validator: checkEmail, required: true, trigger: "blur" }],
      tel: [{ validator: checkTel, required: true, trigger: "blur" }],
	  },
	  rule1: {
        passwd: [{ validator: checkPWD, required: true, trigger: "blur" }],
		    email: [{ validator: checkEmail, required: true, trigger: "blur" }],
        repeatPasswd: [{ validator: checkPWD, required: true, trigger: "blur" }]
      },
    };
  },
  created() {
    this.getValidcode();
  },
  beforeUpdate() {
    this.$nextTick(function () {
      this.autolog = this.$route.query.id;
      if (this.autolog === "autoTestingV1") {
        this.$store.commit("system/validationFilling", this.validcode.value);
      }
    });
  },
  computed: {
    username: {
      get() {
        return this.$store.state.system.login.username;
      },
      set(value) {
        this.$store.commit("system/settersLogin", {
          key: "username",
          value: value,
        });
      },
    },
    password: {
      get() {
        return this.$store.state.system.login.password;
      },
      set(value) {
        this.$store.commit("system/settersLogin", {
          key: "password",
          value: value,
        });
      },
    },
    validcodeInput: {
      get() {
        return this.$store.state.system.login.validcodeInput;
      },
      set(value) {
        this.$store.commit("system/settersLogin", {
          key: "validcodeInput",
          value: value,
        });
      },
    },
    validcode: {
      get() {
        return this.$store.state.system.login.validcode;
      },
      set(value) {
        this.$store.commit("system/settersLogin", {
          key: "validcode",
          value: value,
        });
      },
    },
  },
  methods: {
    showSignUpDialog() {
      this.dialogVisible = true;
    },
    showForgetDialog () {
        this.dialogVisible1 = true;
    },
    handleClose() {
      this.dialogVisible = false;
    },
    handleClose1 () {
        this.dialogVisible1 = false;
    },
    getValidcode() {
      // 更换验证码
      this.$store.dispatch("system/validcode");
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
	  submitForm1 (formName) {
      this.$refs['forgetForm'].validate((valid) => {
        if (valid) {
            // this.$store.dispatch('otherk/editdata', this.forgetForm)
        } else {
          return false;
        }
      })
    },
    submit: debounce(
      function () {
        // 登录
        let data = {
          username: compileStr(this.username),
          password: compileStr(this.password),
          validcode: compileStr(this.validcodeInput),
          originalStr: this.validcode.originalStr,
        };
        if (this.username.replace(/(^\s*)|(\s*$)/g, "") == "") {
          Notification.error({
            title: "登录失败",
            message: "用户名不能为空",
          });
          this.$store.dispatch("system/validcode");
        } else if (this.password.replace(/(^\s*)|(\s*$)/g, "") == "") {
          Notification.error({
            title: "登录失败",
            message: "密码不能为空",
          });
          this.$store.dispatch("system/validcode");
        } else if (this.validcodeInput.replace(/(^\s*)|(\s*$)/g, "") == "") {
          Notification.error({
            title: "登录失败",
            message: "验证码不能为空",
          });
          this.$store.dispatch("system/validcode");
        } else {
          this.$store.dispatch("system/login", data);
        }
        this.$router.push({name: '地理位置分析'})
      },
      2000,
      true
    ),
    changeValue(key, value) {
      // 获取用户名、密码、验证码
      if (key === "validcodeInput") {
        this.validcodeTest = true;
      }
      let data = {
        key: key,
        value: value,
      };
      this.$store.commit("system/settersLogin", data);
    },
  },
  watch: {
    $route() {
      this.autolog = this.$route.query.id;
      if (this.autolog === "autoTestingV1") {
        this.$store.commit("system/validationFilling", this.validcode.value);
      }
    },
  },
};
</script>
<style scoped>
#container {
  background-color: #e5eaf1;
}
#va {
  width: 70%;
  float: left;
}
.cls-content .form-group {
  margin-bottom: 12px;
}
.input-group input {
  border: none;
}
#loginButton {
  padding: 8px 16px;
  background-color: #4990ff;
  border-color: #4990ff;
  font-size: 15px;
  font-weight: 100;
}
#loginButton:hover {
  padding: 8px 16px;
  background-color: #3761f4;
  border-color: #3761f4;
  font-size: 15px;
  font-weight: 100;
}
.input-group input:focus {
  border: none;
}
.input-group-addon {
  min-width: 36px;
  padding: 6px 0px 6px 10px;
}
#vaImg {
  width: 30%;
  height: 39px;
  float: left;
}
.clearFloat {
  clear: both;
}
.pad-btm {
  padding-bottom: 37px;
}
.showTips {
  text-align: left !important;
}
.showError {
  display: none;
}
.cls-container {
  background-color: #f8f8f8;
  /* background-image: url('../../images/login/bg.jpg'); */
  /* background-size: 100% 100%; */
  position: relative;
}
.cls-content {
  padding-top: 80px;
  /* background: #ecf0f5;
  padding-bottom: 345px */
}
.mar-ver {
  margin-top: 95px;
  margin-bottom: 15px;
}
.mar-ver h3 {
  font-size: 20px;
  color: #ebebeb;
  font-weight: 100;
  font-family: "Microsoft YaHei";
  margin-top: 30px;
}
.cls-content .cls-content-sm {
  width: 390px;
}
.form-control {
  height: 39px;
}
.input-group-addon {
  background-color: #fff;
}
</style>
