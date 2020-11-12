<template>
    <div style='margin:20px;padding:20px;background:#fff'>
        <el-table :data='tableDataRepaire'>
            <el-table-column prop='' label='序号'>
                <template slot-scope="scope">
                    <div>
                        {{scope.$index + 1}}
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop='age' label='年龄'></el-table-column>
            <el-table-column prop='sex' label='性别'></el-table-column>
            <el-table-column prop='address' label='家庭住址'></el-table-column>
            <el-table-column prop='email' label='邮箱'></el-table-column>
            <el-table-column prop='role' label='角色'></el-table-column>
            <el-table-column prop='call' label='电话'></el-table-column>
            <el-table-column prop='time' label='注册时间'></el-table-column>
            <el-table-column prop='' label='操作'>
                <template slot-scope='scope'>
                    <div>
                        <span @click='showResetDialog(scope.row)'>
                            恢复
                        </span>
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog
            title="个人信息修改"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="close"
        >
            <span>
                是否恢复该用户
            </span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="resetData"
                >确 定</el-button
                >
            </span>
        </el-dialog>
    </div>
</template>
<script>
import {mapState} from 'vuex'
export default{
    data () {
        return {
            dialogVisible: false
        }
    },
    computed:{
        ...mapState({
            tableDataRepaire: state=> state.usermanage.tableDataRepaire
        })
    },
    created () {
        this.$store.dispatch('usermanage/GET_REPAIRE_DATA')
    },
    methods:{
        showResetDialog (row) {
            this.row = row
            this.dialogVisible = true
        },
        resetData () {
            this.$store.dispatch('', this.row)
            this.dialogVisible = false
        },
        close () {
            this.dialogVisible = false
        }
    }
}
</script>