<template>
    <div style='width:100%;height:100%'>
        <el-date-picker @change='timeChange' v-model='timerange' style='position: absolute;z-index: 1;' type="daterange" range-separator="至"></el-date-picker>
        <div id='chinaMap' style='width:100%;height:100%'>

        </div>
    </div>
</template>
<script>
import config from '../components/mapConfig.js'
import $http from '../utils/http.js'
import axios from 'axios'
import echarts from 'Echarts'
import {mapState} from 'vuex'
export default {
    data () {
        return {
            config: config,
            timerange: []
        }
    },
    computed:{
        ...mapState({
            location_data: state=> state.location.location_data,
            showFlag: state=> state.location.showFlag,
        })
    },
    // async mounted () {
    //     debugger
    //     console.log(this.location_data)
    //     await this.initEcharts()
    // },
    watch:{
        showFlag (newV, oldV) {
            if(newV){
                this.initEcharts()
            }
        }
    },
    created () {
        this.$store.dispatch('location/GET_CHART_DATA')
    },
    methods:{
        timeChange () {
            this.$store.dispatch('location/GET_CHART_DATA', {start_time: this.timerange[0], end_time: this.timerange[1]})
        },
        initEcharts () {
            const myChart = echarts.init(document.getElementById('chinaMap'))
            var year = ["2020"];
            var mapData = []
            /*柱子Y名称*/
            var categoryData = [];
            var barData = [];
            console.log(this.location_data)
            for (var key in config.geoCoordMap) {
                console.log(this.location_data)
                mapData.push({
                    "year": '2020',
                    "name": key,
                    "value": this.location_data[key],
                });
                
            }
            for (var i = 0; i < mapData.length; i++) {
                mapData.sort(function sortNumber(a, b) {
                    return a.value - b.value
                });
                barData.push([]);
                categoryData.push([]);
                for (var j = 0; j < mapData.length; j++) {
                    barData[i].push(mapData[j].value);
                    categoryData[i].push(mapData[j].name);
                }
            }
            echarts.registerMap('china', config.geoJson);
            var convertData = function(data) {
                var res = [];
                for (var i = 0; i < data.length; i++) {
                    var geoCoord = config.geoCoordMap[data[i].name];
                    if (geoCoord) {
                        res.push({
                            name: data[i].name,
                            value: geoCoord.concat(data[i].value)
                        });
                    }
                }
                return res;
            };
            var optionXyMap01 = {
                timeline: {
                    data: year,
                    axisType: 'category',
                    autoPlay: true,
                    playInterval: 3000,
                    left: '10%',
                    right: '10%',
                    bottom: '3%',
                    width: '80%',
                    
                    label: {
                        normal: {
                            textStyle: {
                                color: '#ddd'
                            }
                        },
                        emphasis: {
                            textStyle: {
                                color: '#fff'
                            }
                        }
                    },
                    symbolSize: 10,
                    lineStyle: {
                        color: '#555'
                    },
                    checkpointStyle: {
                        borderColor: '#777',
                        borderWidth: 2
                    },
                    controlStyle: {
                        showNextBtn: true,
                        showPrevBtn: true,
                        normal: {
                            color: '#666',
                            borderColor: '#666'
                        },
                        emphasis: {
                            color: '#aaa',
                            borderColor: '#aaa'
                        }
                    },

                },
                baseOption: {
                    animation: true,
                    animationDuration: 1000,
                    animationEasing: 'cubicInOut',
                    animationDurationUpdate: 1000,
                    animationEasingUpdate: 'cubicInOut',
                    grid: {
                        right: '1%',
                        top: '15%',
                        bottom: '10%',
                        width: '20%'
                    },
                    tooltip: {
                        trigger: 'axis', // hover触发器
                        axisPointer: { // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                            shadowStyle: {
                                color: 'rgba(150,150,150,0.1)' //hover颜色
                            }
                        }
                    },
                    geo: {
                        show: true,
                        map: 'china',
                        roam: true,
                        zoom: 1,
                        center: [113.83531246, 34.0267395887],
                        label: {
                            emphasis: {
                                show: false
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: 'rgba(147, 235, 248, 1)',
                                borderWidth: 1,
                                areaColor: {
                                    type: 'radial',
                                    x: 0.5,
                                    y: 0.5,
                                    r: 0.8,
                                    colorStops: [{
                                        offset: 0,
                                        color: 'rgba(147, 235, 248, 0)' // 0% 处的颜色
                                    }, {
                                        offset: 1,
                                        color: 'rgba(147, 235, 248, .2)' // 100% 处的颜色
                                    }],
                                    globalCoord: false // 缺省为 false
                                },
                                shadowColor: 'rgba(128, 217, 248, 1)',
                                // shadowColor: 'rgba(255, 255, 255, 1)',
                                shadowOffsetX: -2,
                                shadowOffsetY: 2,
                                shadowBlur: 10
                            },
                            emphasis: {
                                areaColor: '#389BB7',
                                borderWidth: 0
                            }
                        }
                    },
                },
                options: []

            };
            for (var n = 0; n < year.length; n++) {
                optionXyMap01.options.push({
                    backgroundColor: '#013954',
                    title:
                        [{
                                left: '25%',
                                top: '7%',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 25
                                }
                            },
                            {
                                id: 'statistic',
                                text: 2020 + "数据统计情况",
                                left: '75%',
                                top: '8%',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 25
                                }
                            }
                        ],
                    xAxis: {
                        type: 'value',
                        scale: true,
                        position: 'top',
                        min: 0,
                        boundaryGap: false,
                        splitLine: {
                            show: false
                        },
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            margin: 2,
                            textStyle: {
                                color: '#aaa'
                            }
                        },
                    },
                    yAxis: {
                        type: 'category',
                        //  name: 'TOP 20',
                        nameGap: 16,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: '#ddd'
                            }
                        },
                        axisTick: {
                            show: false,
                            lineStyle: {
                                color: '#ddd'
                            }
                        },
                        axisLabel: {
                            interval: 0,
                            textStyle: {
                                color: '#ddd'
                            }
                        },
                        data: categoryData[n]
                    },
                    series: [
                        //地图
                        {
                            type: 'map',
                            map: 'china',
                            geoIndex: 0,
                            aspectScale: 0.75, //长宽比
                            showLegendSymbol: false, // 存在legend时显示
                            label: {
                                normal: {
                                    show: false
                                },
                                emphasis: {
                                    show: false,
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            roam: true,
                            itemStyle: {
                                normal: {
                                    areaColor: '#031525',
                                    borderColor: '#FFFFFF',
                                },
                                emphasis: {
                                    areaColor: '#2B91B7'
                                }
                            },
                            animation: false,
                            data: mapData
                        },
                        //地图中闪烁的点
                        {
                            //  name: 'Top 5',
                            type: 'effectScatter',
                            coordinateSystem: 'geo',
                            data: convertData(mapData.sort(function(a, b) {
                                return b.value - a.value;
                            }).slice(0, 20)),
                            symbolSize: function(val) {
                                return val[2] / 20;
                            },
                            showEffectOn: 'render',
                            rippleEffect: {
                                brushType: 'stroke'
                            },
                            hoverAnimation: true,
                            label: {
                                normal: {
                                    formatter: '{b}',
                                    position: 'right',
                                    show: true
                                }
                            },
                            itemStyle: {
                                normal: {
                                    color: config.colors[config.colorIndex][n],
                                    shadowBlur: 10,
                                    shadowColor: config.colors[config.colorIndex][n]
                                }
                            },
                            zlevel: 1
                        },
                        //柱状图
                        {
                            zlevel: 1.5,
                            type: 'bar',
                            symbol: 'none',
                            itemStyle: {
                                normal: {
                                    color: config.colors[config.colorIndex][n]
                                }
                            },
                            data: barData[n]
                        }
                    ]
                })
            }
            myChart.setOption(optionXyMap01);
        }
    }
}
</script>
<style>
    
</style>