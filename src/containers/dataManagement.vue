<template>
    <div id='dataManagement' style='padding:20px'>
        <div style='padding:10px;background-color: #fff;margin-bottom:20px'>
            <h4>
                商品下单数量走势分析
            </h4>
            <div id='lineBar' style='width:100%;height: 400px;'>
            </div>
        </div>
        <div style='padding:20px;background:#fff'>
            <el-input type='search' v-model='value' style='width:400px;float:right' suffix-icon='el-icon-search' @change='searchTable'>
            </el-input>
            <el-button type='primary' id='downBtn' @click='exportExcl()'>
                数据下载
            </el-button>
            <div style='clear:both'>

            </div>
            <el-table style='margin-top:20px' id='exportTable' :data='tableData'>
                <el-table-column prop='date' label='序号'></el-table-column>
                <el-table-column prop='name' label='用户ID'></el-table-column>
                <el-table-column prop='address' label='商品ID'></el-table-column>
                <el-table-column prop='' label='用户行为类型'></el-table-column>
                <el-table-column prop='' label='地理位置经度'></el-table-column>
                <el-table-column prop='' label='地理位置纬度'></el-table-column>
                <el-table-column prop='' label='商品类别ID'></el-table-column>
                <el-table-column prop='' label='记录时间'></el-table-column>
            </el-table>
        </div>
        
    </div>
</template>
<script>
    import {mapState} from 'vuex'
    import FileSaver from "file-saver";
    import XLSX from "xlsx";
    import echarts from 'Echarts'
    export default{
        data () {
            return {
                value: '',
                tableData: [{
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1517 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄'
                }]
            }
        },
        mounted () {
            this.initEcharts()
        },
        methods:{
            initEcharts () {
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
                        show: false,
                        type: 'category',
                        boundaryGap: false,
                        data: date
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
                        data: data
                    }]
                };
                myChart.setOption(option)
            },
            searchTable () {
                this.$store.commit('')
                this.$store.dispatch()
            },
            exportExcl () {
                //blob URL形式文件下载
                /* 从表生成工作簿对象 */
                var wb = XLSX.utils.table_to_book(document.querySelector("#exportTable"));
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
            }
        }
    }
</script>