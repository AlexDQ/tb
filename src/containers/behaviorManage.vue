<template>
    <div id='behaviorManage'>
        <div style='width:380px;height:350px;background-color: #fff;'>
            <h4>用户行为类型占比分析</h4>
            <div id='pieBehavior' style='width:300px;height:300px'>
            </div>
        </div>
        <div style='margin:20px;padding:20px;background:#fff'>
            <el-button type='primary' @click='showAddDialog'>新增</el-button>
            <el-button type='primary' @click='downloadExcel'>数据下载</el-button>
            <el-table id='behaviorTable'>
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
import FileSaver from "file-saver";
import XLSX from "xlsx";
import echarts from 'Echarts'
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
    mounted () {
        this.initEcharts()
    },
    methods:{
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
                    data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎']
                },
                series: [
                    {
                        name: '访问来源',
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
                        data: [
                            {value: 335, name: '直接访问'},
                            {value: 310, name: '邮件营销'},
                            {value: 234, name: '联盟广告'},
                            {value: 135, name: '视频广告'},
                            {value: 1548, name: '搜索引擎'}
                        ]
                    }
                ]
            };
            myChart.setOption(option)
        },
        showAddDialog() {
            this.dialogVisible = true
        },
        submitForm () {
            if(!this.form.name){
                Notification.error('请填写类别名称')
            }
        },
        downloadExcel () {
            var wb = XLSX.utils.table_to_book(document.querySelector("#behaviorTable"));
            /* 获取二进制字符串作为输出 */
            var wbout = XLSX.write(wb, {
                bookType: "xlsx",
                bookSST: true,
                type: "array"
            });
            try {
                FileSaver.saveAs(
                //Blob 对象表示一个不可变、原始数据的类文件对象。
                //Blob 表示的不一定是JavaScript原生格式的数据。
                //File 接口基于Blob，继承了 blob 的功能并将其扩展使其支持用户系统上的文件。
                //返回一个新创建的 Blob 对象，其内容由参数中给定的数组串联组成。
                new Blob([wbout], { type: "application/octet-stream" }),
                //设置导出文件名称
                "sheetjs.xlsx"
                );
            } catch (e) {
                if (typeof console !== "undefined") console.log(e, wbout);
            }
            return wbout;
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