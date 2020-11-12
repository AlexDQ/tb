<template>
    <div id='dataManagement' style='padding:20px'>
        <el-select v-model='form.behavior_type' placeholder='请选择行为类型' @change='selectChange'>
            <el-option label='点击' value='1'></el-option>
            <el-option label='收藏' value='2'></el-option>
            <el-option label='加入购物车' value='3'></el-option>
            <el-option label='购买' value='4'></el-option>
        </el-select>
        <el-input type='search' 
            v-model='form.item_id' 
            style='width:400px;margin-bottom:20px' 
            placeholder='请搜索商品ID'
            suffix-icon='el-icon-search' 
            @keyup.enter.native='searchTable'>
        </el-input>
        <div style='padding:10px;background-color: #fff;margin-bottom:20px'>
            <h4>
                商品下单数量走势分析
            </h4>
            
            <div id='lineBar' style='width:100%;height: 400px;'>
            </div>
        </div>
        <div style='padding:20px;background:#fff'>
            <el-button type='primary' id='downBtn' @click='exportExcl()'>
                数据下载
            </el-button>
            <el-button type='primary' @click='showAddDialog'>新增</el-button>
            <div style='clear:both'>

            </div>
            <el-table style='margin-top:20px' id='exportTable' :data='tableData'>
                <el-table-column prop='date' label='序号'>
                    <template slot-scope='scope'>
                        <div>
                            {{scope.$index + 1}}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop='name' label='用户ID'></el-table-column>
                <el-table-column prop='address' label='商品ID'></el-table-column>
                <el-table-column prop='' label='用户行为类型'></el-table-column>
                <el-table-column prop='' label='地理位置经度'></el-table-column>
                <el-table-column prop='' label='地理位置纬度'></el-table-column>
                <el-table-column prop='' label='商品类别ID'></el-table-column>
                <el-table-column prop='' label='记录时间'></el-table-column>
            </el-table>
        </div>
        <el-dialog
            :title="type"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="close"
            >
            <el-form ref="datafrom" :model="dataform" :rules="rule">
                <el-form-item prop="item_id" label="商品ID">
                    <el-input v-model="dataform.item_id"></el-input>
                </el-form-item>
                <el-form-item prop="item_category" label="商品类别">
                    <el-input v-model="dataform.item_category"></el-input>
                </el-form-item>
                <el-form-item prop="r_time" label="时间">
                    <el-date-picker format='yyyy-MM-dd hh:mm:ss' v-model="dataform.r_time"></el-date-picker>
                </el-form-item>
                <el-form-item prop="behavior_type" label="用户行为类型">
                    <el-select v-model="dataform.behavior_type">
                        <el-option label='点击' value='1'></el-option>
                        <el-option label='收藏' value='2'></el-option>
                        <el-option label='加入购物车' value='3'></el-option>
                        <el-option label='购买' value='4'></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item prop="longitude" label="经度">
                <el-input v-model="dataform.longitude"></el-input>
                </el-form-item>
                <el-form-item prop="latitude" label="纬度">
                <el-input v-model="dataform.latitude"></el-input>
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
    import FileSaver from "file-saver";
    import XLSX from "xlsx";
    import echarts from 'Echarts'
    export default{
        data () {
            let checkName = (rule, value, callback) => {
                if (value === "" || value === null) {
                    callback(new Error("请输入商品ID"));
                } else {
                    callback();
                }
            }
            return {
                value: '',
                dialogVisible: false,
                row:{},
                type: 'add',
                rule: {
                    item_id: [{ validator: checkName, required: true, trigger: "blur" }],
                    // call: [{ validator: checkTel, required: false, trigger: "blur" }],
                },
            }
        },
        computed:{
            ...mapState({
                tableData: state => state.salesmanage.tableData,
                form: state=> state.salesmanage.form,
                showFlag:  state=> state.salesmanage.showFlag,
                xdata:  state=> state.salesmanage.xdata,
                ydata:  state=> state.salesmanage.ydata,
                dataform: state => state.salesmanage.dataform
            })
        },
        created () {
            // this.$store.dispatch('salesmanage/GET_TABLE_DATA')
            this.$store.dispatch('salesmanage/GET_CHART_DATA')
        },
        watch:{
            showFlag (newV, oldV) {
                if(newV){
                    this.initEcharts()
                }
            },
        },
        mounted () {
            this.initEcharts()
        },
        methods:{
            etNowFormatDate(d) {
                var date = d;
                var seperator1 = "-";
                var seperator2 = ":";
                var month = date.getMonth() + 1;
                var strDate = date.getDate();
                if (month >= 1 && month <= 9) {
                    month = "0" + month;
                }
                if (strDate >= 0 && strDate <= 9) {
                    strDate = "0" + strDate;
                }
                var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
                        + " " + date.getHours() + seperator2 + date.getMinutes()
                        + seperator2 + date.getSeconds();
                return currentdate;
            },
            showAddDialog () {
                this.dialogVisible = true
            },
            close () {
                this.dialogVisible = false
            },
            submitForm (formName) {
                this.$refs['datafrom'].validate((valid) => {
                    if (valid) {
                        if(this.type == 'edit'){
                            Object.assign(this.datafrom, {id: this.row.id})
                        }
                        this.dataform.r_time = this.etNowFormatDate(this.dataform.r_time) 
                        this.$store.dispatch('salesmanage/SUBMIT_FORM_DATA', this.dataform)
                        this.dialogVisible = false
                    } else {
                        this.dialogVisible = false
                        return false;
                    }
                })
            },
            deleteSubmit () {
                this.$store.dispatch('usermanage/DETLET_USER_DATA', {id:this.row1.login_id})
                this.showDeleteDialog = false
            },
            showEditDialog (type, row) {
                this.type = type
                this.dialogVisible = true
                this.row = row
                this.datafrom = Object.assign(row, {})
            },
            selectChange (val) {
                this.$store.dispatch('salesmanage/GET_TABLE_DATA')
            },
            initEcharts ()  {
                const myChart = echarts.init(document.getElementById('lineBar'))
                var base = +new Date(2020, 9, 1);
                var interval = 24 * 3600 * 1000;
                var now = new Date(base); // 时间
                var date = [getTime(now)];
                var data = [15]; // 初始数据 
                for (var i = 1; i < 30; i++) {
                    now = new Date(base += interval);
                    let r = Math.random();
                    let c1 = -0.5; // 系数1: 增减趋势概率
                    let c2 = 5; // 系数2: 幅度 倍数
                    date.push(getTime(now));
                    data.push(Math.round((r + c1) * c2 + data[i - 1]));
                }
                function getTime(now) {
                    return [now.getFullYear(), now.getMonth(), now.getDate()].join('-');
                }
                let option = {
                    grid: {
                        left: "0%",
                        right: "5%",
                        bottom: "0%",
                        containLabel: true
                    },
                    tooltip: {
                        show: true,
                        trigger: 'axis',
                        position: function(pt) {
                            return [pt[0], '10%'];
                        }
                    },
                    toolbox: {
                        show: false,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        show: true,
                        type: 'category',
                        boundaryGap: false,
                        data: this.xdata
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '100%']
                    },
                    dataZoom: [{
                        show: false,
                        type: 'inside',
                        start: 0,
                        end: 100
                        }, 
                        {
                            show: false,
                            start: 0,
                            end: 100,
                            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                            handleSize: '80%',
                            handleStyle: {
                                color: '#fff',
                                shadowBlur: 3,
                                shadowColor: 'rgba(0, 0, 0, 0.6)',
                                shadowOffsetX: 2,
                                shadowOffsetY: 2
                            }
                        }
                    ],
                    series: [{
                        markPoint: {
                            data: [{
                                    type: 'max',
                                    name: '最大值'
                                },
                                {
                                    type: 'min',
                                    name: '最小值'
                                }
                            ]
                        },
                        name: '模拟数据',
                        type: 'line',
                        smooth: true,
                        symbol: 'none',
                        sampling: 'average',
                        itemStyle: {
                            color: 'rgb(255, 70, 131)'
                        },
                        areaStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgb(255, 158, 68)'
                            }, {
                                offset: 1,
                                color: 'rgb(255, 70, 131)'
                            }])
                        },
                        data: this.ydata
                    }]
                };
                myChart.setOption(option)
            },
            searchTable () {
                this.$store.commit('')
                this.$store.dispatch()
            },
            exportExcl () {
                this.$store.dispatch('salesmanage/DOWNLOAD_CSV_DATA')
            }
        }
    }
</script>