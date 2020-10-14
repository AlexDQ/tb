<template>
    <div>
        <el-button type='primary' @click='showAddDialog'>数据下载</el-button>
        <el-button type='primary' @click='showAddDialog'>新增</el-button>
        <el-button type='primary' @clcik='deleteItem'>删除</el-button>
        <el-table>
            <el-table-column prop='' label=''></el-table-column>
            <el-table-column prop='' label=''></el-table-column>
            <el-table-column prop='' label=''></el-table-column>
            <el-table-column prop='' label=''></el-table-column>
            <el-table-column prop='' label=''>
                <template>
                    <div>
                        <span>
                            删除
                        </span>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<script>
export default {
    data () {

    },
    methods:{
        deleteItem () {

        },
        showAddDialog () {

        }
    }
}
</script>