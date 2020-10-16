<template>
    <div id='behaviorManage'>
        <div style='margin:20px;padding:20px;background:#fff'>
            <el-button type='primary' @click='showAddDialog'>新增</el-button>
            <el-table>
                <el-table-column prop='' label='序号'></el-table-column>
                <el-table-column prop='' label='类别名称'></el-table-column>
                <el-table-column prop='' label='添加人'></el-table-column>
                <el-table-column prop='' label='记录时间'></el-table-column>
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
                    是否删除该用户行为
                </span>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogVisible1 = false">取 消</el-button>
                    <el-button type="primary" @click="deleteSubmit"
                    >确 定</el-button
                    >
                </span>
            </el-dialog>
            <el-dialog
                title="新增"
                :visible.sync="dialogVisible"
                width="30%"
                :before-close="close"
                
                >
                <el-form ref="ruleForm" :model="form">
                    <el-form-item prop="name" label="类别">
                        <el-input style='width:400px' v-model="form.name"></el-input>
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
    </div>
</template>
<script>
import {Notification} from 'element-ui'
export default{
    data () {
        return {
            form:{
                name: ''
            },
            dialogVisible: false,
            dialogVisible1: false,
        }
    },
    methods:{
        showAddDialog() {
            this.dialogVisible = true
        },
        submitForm () {
            if(!this.form.name){
                Notification.error('请填写类别名称')
            }
        },
        deleteSubmit () {
            
        },
        close () {
            
        },
        close1 () {

        }
    }
}
</script>