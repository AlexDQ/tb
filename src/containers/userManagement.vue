<template>
    <div style='margin:20px;padding:20px;background:#fff'>
        <el-button type='primary' @click='showAddDialog("add")'>新增用户</el-button>
        <el-button type='primary' @click='showDeleteDialog1'>删除</el-button>
        <el-table @selection-change='selectChange' :data='userData'>
            <el-table-column type='selection'></el-table-column>
            <el-table-column prop='' label='序号'>
                <template slot-scope='scope'>
                    <div>   
                        {{scope.$index + 1}}
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop='name' label='姓名'></el-table-column>
            <el-table-column prop='age' label='年龄'></el-table-column>
            <el-table-column prop='sex' label='性别'></el-table-column>
            <el-table-column prop='address' label='家庭住址'></el-table-column>
            <el-table-column prop='email' label='邮箱'></el-table-column>
            <el-table-column prop='role' label='角色'></el-table-column>
            <el-table-column prop='call' label='电话'></el-table-column>
            <el-table-column prop='time' label='注册时间'></el-table-column>
            <el-table-column prop='' label='操作'>
                <template slot-scope='scope'>
                    <div style='color:#409EFF;cursor:pointer'>
                        <span @click='showEditDialog("edit", scope.row)'>编辑</span>&nbsp;&nbsp;
                        <span @click='showResetPwdDialog(scope.row)'>重置密码</span>&nbsp;&nbsp;
                        <span @click='showDeleteDialog(scope.row)'>删除</span>&nbsp;&nbsp;
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            @size-change="SizeChange"
            @current-change="CurrentChange"
            :currentPage="pageNo"
            :total="total"
            :pageSizes="[10, 20, 40]"
            :pageSize="pageSize"
            style="text-align: center;margin-top:20px"
            layout="total, sizes, prev, pager, next"
        >

        </el-pagination>
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
            title="删除"
            :visible.sync="dialogDeleteVisible"
            width="30%"
            :before-close="close2"
            >
            <span>
                是否删除该用户
            </span>
            <span slot='footer'>
                <el-button @click='dialogDeleteVisible = false'>取消</el-button>
                <el-button @click='submitDelete'>确定</el-button>
            </span>
        </el-dialog>
        <el-dialog
            :title="type"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="close"
            >
            <el-form ref="signUpForm" :model="signUpForm" :rules="rule">
                <el-form-item prop="name" label="姓名">
                <el-input v-model="signUpForm.name"></el-input>
                </el-form-item>
                <el-form-item prop="email" label="邮箱">
                <el-input v-model="signUpForm.email"></el-input>
                </el-form-item>
                <el-form-item prop="call" label="电话">
                <el-input v-model="signUpForm.call"></el-input>
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
import {mapState} from 'vuex'
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
            var regex = new RegExp("^1[3456789]d{9}$");
            if (!regex.test(value)) {
                callback(new Error("请输入正确格式的手机号码"));
            } else {
                callback();
            }
        };
        let checkEmail = (rule, value, callback) => {
            var regex = new RegExp("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$");
            if (!regex.test(value)) {
                callback(new Error("请输入正确格式的电子邮箱"));
            } else {
                callback();
            }
        };
        return{
            selectList:'',
            dialogVisible: false,
            dialogVisible1: false,
            dialogDeleteVisible: false,
            signUpForm: {
                call: "",
                email: "",
                address: "",
                age: "",
                sex: "",
                name: "",
            },
            rule: {
                name: [{ validator: checkName, required: true, trigger: "blur" }],
                email: [{ validator: checkEmail, required: true, trigger: "blur" }],
                // call: [{ validator: checkTel, required: false, trigger: "blur" }],
            },
            row1: {},
            row:{},
            type: 'add'
        }
    },
    computed:{
        ...mapState({
            userData: state=>state.usermanage.userData,
            pageSize: state => state.usermanage.pageSize,
            pageNo: state => state.usermanage.pageNo,
            total: state => state.usermanage.total
        }),
    },
    watch:{
        dialogVisible (newV, oldV) {
            if(!newV){
                this.$refs.signUpForm.resetFields()
            }
        }
    },
    created(){
        this.$store.dispatch('usermanage/GET_USER_LIST')
    },
    methods:{
        selectChange (val) {
            let temp = []
            val.forEach((item, index)=>{
                temp.push(item.login_id)
            })
            this.selectList = temp.join(',')
        },
        submitDelete () {
            this.$store.dispatch('usermanage/DETLET_USER_DATA', {id: this.selectList})
            this.dialogDeleteVisible = false
        },
        showDeleteDialog1 () {
            this.dialogDeleteVisible = true
        },
        SizeChange (val) {
            this.$store.commit('usermanage/SET_PAGE_CHANGE', {key: 'pageSize', val: val})
        },
        CurrentChange (val) {
            this.$store.commit('usermanage/SET_PAGE_CHANGE', {key: 'pageNo', val: val})
        },
        close1 () {
            this.dialogVisible1 = false
        },
        close2 () {
            this.dialogDeleteVisible = false
        },
        deleteSubmit () {
            this.$store.dispatch('usermanage/DETLET_USER_DATA', {id:this.row1.login_id})
            this.showDeleteDialog = false
        },
        showAddDialog (type) {
            this.type = type            
            this.dialogVisible = true
        },
        showEditDialog (type, row) {
            this.type = type
            this.dialogVisible = true
            this.row = row
            this.signUpForm = Object.assign(row, {})
        },
        close () {
            this.dialogVisible = false
        },
        submitForm (formName) {
            this.$refs['signUpForm'].validate((valid) => {
                if (valid) {
                    if(this.type == 'edit'){
                        Object.assign(this.signUpForm, {login_id: this.row.login_id})
                    }
                    this.$store.dispatch('usermanage/EDIT_USER_DATA', this.signUpForm)
                    this.dialogVisible = false
                } else {
                    this.dialogVisible = false
                    return false;
                }
            })
        },
        showResetPwdDialog (row) {
            this.$store.dispatch('usermanage/RESET_USER_PASSWD', {login_id: row.login_id})
        },
        showDeleteDialog (row) {
            this.dialogVisible1 = true
            this.row1 = row
        }
    }
}
</script>