<template>
    <div id='behaviorManage'>
        <div style='width:380px;height:350px;background-color: #fff;margin:20px 0 0 20px'>
            <h4 style='text-indent:20px'>用户行为类型占比分析</h4>
            <div id='pieBehavior' style='width:300px;height:300px'>
            </div>
        </div>
        <div style='margin:20px;padding:20px;background:#fff'>
            <el-button type='primary' @click='showAddDialog'>新增</el-button>
            <el-button type='primary' @click='dialogVisible1 = true'>删除</el-button>
            <el-button type='primary' @click='downloadExcel'>数据下载</el-button>
            <!-- {{behaviorData}} -->
            <el-table id='behaviorTable' :data='behaviorData' @selection-change='selectChange'>
                <el-table-column type='selection'></el-table-column>
                <el-table-column prop='' label='序号'>
                    <template slot-scope='scope'>
                        <div>
                            {{scope.$index + 1}}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop='name' label='类别名称'>
                    <!-- <template slot-scope="scope">
                        <div>
                            {{scope.row.name ==1 ? "点击" : scope.row.name == 2 ? "收藏" : scope.row.name == 3 ? "加入购物车" : "购买"}}   
                        </div>
                    </template> -->
                </el-table-column>
                <el-table-column prop='username' label='添加人'></el-table-column>
                <el-table-column prop='time' label='记录时间'></el-table-column>
                <el-table-column prop='' label='操作'>
                    <template slot-scope='scope'>
                        <div style='color:#4099ff'>
                            <span @click='showEditDialog(scope.row)'>编辑</span>
                            <!-- <span @click='showResetPwdDialog(scope.row)'>重置密码</span> -->
                            <span @click='showDeleteDialog(scope.row)'>删除</span>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog
                title="删除"
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
import {mapState} from 'vuex'
import FileSaver from "file-saver";
import XLSX from "xlsx";
import $http from './../utils/http'
import echarts from 'Echarts'
export default{
    data () {
        return {
            form:{
                name: ''
            },
            dialogVisible: false,
            dialogVisible1: false,
            tempList: [],
            row: {},
            type: 'add'
        }
    },
    watch:{
        showFlag(newV, oldV){
            if(newV){
                this.initEcharts()
            }
        }
    },
    created () {
        this.$store.dispatch('salesmanage/GET_PIE_DATA')
        this.$store.dispatch('salesmanage/GET_BEHAVIOR_DATA')
    },
    mounted () {
        this.initEcharts()
    },
    computed:{
        ...mapState({
            showFlag: state=>state.salesmanage.showFlag1,
            piexdata: state=>state.salesmanage.piexdata,
            pieydata: state=>state.salesmanage.pieydata,
            behaviorData: state => state.salesmanage.behaviorData
        })
    },
    methods:{
        selectChange (val) {
            val.forEach((item, index)=>{
                this.tempList.push(item.id)
            })
        },
        showEditDialog (row) {
            this.type = 'edit'
            this.dialogVisible = true
            this.form = row
            this.row = row
        },
        initEcharts () {
            const myChart = echarts.init(document.getElementById('pieBehavior'))
            let option = {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    data: this.piexdata
                },
                series: [
                    {
                        type: 'pie',
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: this.pieydata
                    }
                ]
            };
            myChart.setOption(option)
        },
        showAddDialog() {
            this.type = 'add'
            this.dialogVisible = true
        },
        submitForm () {
            if(!this.form.name){
                Notification.error('请填写类别名称')
            } else {
                if(this.type == 'edit'){
                    Object.assign(this.form, {id: this.row.id})
                }
                Object.assign(this.form, {login_id: localStorage.getItem('userId')})
                this.$store.dispatch('salesmanage/ADD_BEHAVIOR_DATA', this.form)
                this.dialogVisible = false
            }
        },
        downloadExcel () {
            $http.post('/api/behaviors/download')
        },
        showDeleteDialog (row) {
            this.dialogVisible1 = true
            this.row = row
        },
        deleteSubmit () {
            if(this.tempList.length>0){
                this.$store.dispatch('salesmanage/DELETE_BEHAVIOR_DATA', {id: this.tempList.join(',')})
            } else {
                this.$store.dispatch('salesmanage/DELETE_BEHAVIOR_DATA', {id: this.row.id})
            }
            this.dialogVisible1 = false
        },
        close () {
            
        },
        close1 () {

        }
    }
}
</script>