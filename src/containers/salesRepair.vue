<template>
    <div style='margin:20px;padding:20px;background:#fff'>
        <el-table :data='tableDataSale'>
            <el-table-column prop='' label='序号'>
                <template slot-scope='scope'>
                    <div>
                        {{scope.$index + 1}}
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop='user_id' label='用户ID'></el-table-column>
            <el-table-column prop='item_id' label='商品ID'></el-table-column>
            <el-table-column prop='behavior_type' label='用户行为类型'></el-table-column>
            <el-table-column prop='longitude' label='地理位置经度'></el-table-column>
            <el-table-column prop='latitude' label='地理位置纬度'></el-table-column>
            <el-table-column prop='item_category' label='商品类别ID'></el-table-column>
            <el-table-column prop='time' label='记录时间'></el-table-column>
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
                >确 定</el-button>
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
    created () {
        this.$store.dispatch('usermanage/GET_SALES_REPAIRE')
    },
    computed:{
        ...mapState({
            tableDataSale: state=> state.usermanage.tableDataSale
        })
    },
    methods:{
        resetData () {
            
        },
        close () {

        }
    }
}
</script>
