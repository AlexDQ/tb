<template>
    <div style='margin:20px;padding:20px;background:#fff'>
        <el-button type='primary' @click='showAddDialog'>新增用户</el-button>
        <el-table>
            <el-table-column prop='' label='序号'></el-table-column>
            <el-table-column prop='' label='年龄'></el-table-column>
            <el-table-column prop='' label='性别'></el-table-column>
            <el-table-column prop='' label='家庭住址'></el-table-column>
            <el-table-column prop='' label='邮箱'></el-table-column>
            <el-table-column prop='' label='角色'></el-table-column>
            <el-table-column prop='' label='电话'></el-table-column>
            <el-table-column prop='' label='注册时间'></el-table-column>
            <el-table-column prop='' label='操作'>
                <template slot-scope='scope'>
                    <div>
                        <span @click='showEditDialog(scope.row)'>编辑</span>
                        <span @click='showResetPwdDialog(scope.row)'>重置密码</span>
                        <span @click='showDeleteDialog(scope.row)'>删除</span>
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog
            title="个人信息修改"
            :visible.sync="dialogVisible1"
            width="30%"
            :before-close="close1"
        >
            <span>
                是否删除该用户
            </span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible1 = false">取 消</el-button>
                <el-button type="primary" @click="deleteSubmit"
                >确 定</el-button
                >
            </span>
        </el-dialog>
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
    </div>
</template>
<script>
export default {
    data () {
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
        return{
            dialogVisible: false,
            dialogVisible1: false,
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
            row1: {},
            row:{}
        }
    },
    methods:{
        close1 () {
            this.dialogVisible1 = false
        }, 
        deleteSubmit () {
            this.$store.dispatch('', this.row1)
        },
        showAddDialog () {
            this.dialogVisible = true
        },
        showEditDialog (row) {
            this.dialogVisible = true
            this.row = row
        },
        close () {
            this.dialogVisible = false
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
        showResetPwdDialog () {

        },
        showDeleteDialog (row) {
            this.dialogVisible1 = true
            this.row1 = row
        }
    }
}
</script>