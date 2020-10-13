<template>
    <div>
        <div id='chinaMap' style='width:100%;height:1000px'>

        </div>
    </div>
</template>
<script>
import config from '../components/mapConfig.js'
import $http from '../utils/http.js'
import axios from 'axios'
import echarts from 'Echarts'
export default {
    data () {
        return {
            config: config
        }
    },
    mounted () {
        this.initEcharts()
    },
    methods:{
        initEcharts () {
            const myChart = echarts.init(document.getElementById('chinaMap'))
            var year = ["2013", "2014", "2015", "2016", "2017", "2018","2019"];
            var mapData = [
                [],
                [],
                [],
                [],
                [],
                [],
                []
            ];

            /*柱子Y名称*/
            var categoryData = [];
            var barData = [];

            for (var key in config.geoCoordMap) {
                mapData[0].push({
                    "year": '2013',
                    "name": key,
                    "value": config.d1[key],
                });
                mapData[1].push({
                    "year": '2014',
                    "name": key,
                    "value": config.d2[key],
                });
                mapData[2].push({
                    "year": '2015',
                    "name": key,
                    "value": config.d3[key],
                });
                mapData[3].push({
                    "year": '2016',
                    "name": key,
                    "value": config.d4[key],
                });
                mapData[4].push({
                    "year": '2017',
                    "name": key,
                    "value": config.d5[key],
                });
                mapData[5].push({
                    "year": '2018',
                    "name": key,
                    "value": config.d6[key],
                });
                mapData[6].push({
                    "year": '2019',
                    "name": key,
                    "value": config.d7[key],
                });
            }

            for (var i = 0; i < mapData.length; i++) {
                mapData[i].sort(function sortNumber(a, b) {
                    return a.value - b.value
                });
                barData.push([]);
                categoryData.push([]);
                for (var j = 0; j < mapData[i].length; j++) {
                    barData[i].push(mapData[i][j].value);
                    categoryData[i].push(mapData[i][j].name);
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
                                text: '跨境电商百度指数',
                                left: '25%',
                                top: '7%',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 25
                                }
                            },
                            {
                                id: 'statistic',
                                text: year[n] + "数据统计情况",
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
                            data: convertData(mapData[n].sort(function(a, b) {
                                return b.value - a.value;
                            }).slice(0, 20)),
                            symbolSize: function(val) {
                                return val[2] / 10;
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