<template>
    <div id='behaviorAnalysis'>
        <div class='charts_wrapper'>
            <h4 style='margin-bottom: 10px;'>
                购买行为习惯分析
            </h4> 
            <div id='loudou' style='width:100%;height:500px;'>

            </div>
        </div>
        <div class='charts_wrapper'>
            <h4 style='margin-bottom: 10px;'>
                基于时间维度行为习惯分析
            </h4> 
            <div id='timeLine' style='width:100%;height:500px;'>
            </div>
        </div>
    </div>
</template>
<script>
    import echarts from 'Echarts'
    export default{
        data () {
            return {
            }
        },
        mounted () {
            this.initEcharts()
            this.initEcharts1()
        },
        methods:{
            initEcharts () {
                const myChart = echarts.init(document.getElementById('loudou'))
                let option = {
                    backgroundColor: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: '#0c0d2b'
                        }, {
                            offset: 0.5,
                            color: '#0a0c3d'
                        }, {
                            offset: 1,
                            color: '#111629'
                        }],
                        globalCoord: false
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c}%"
                    },
                    legend: {
                        data: ['A', 'B', 'C', 'D', 'E'],
                        x: 'center',
                        y: '92%',
                        textStyle: {
                            color: '#FFF'
                        }
                    },
                    color: ['#c2c1bd', '#00a1e5', '#23c768', '#e5ce10', '#ff7e00', '#fe0000', ],
                    series: [
                        {
                            name: 'TIT',
                            type: 'funnel',
                            left: 'center',
                            width: '90%',
                            sort: 'ascending',
                            label: {
                                normal: {
                                    formatter: '{b}',
                                },

                            },
                            labelLine: {
                                normal: {
                                    show: true,
                                    length: 30
                                }
                            },
                            itemStyle: {
                                normal: {
                                    opacity: 0.3
                                }
                            },
                            tooltip: {
                                show: false
                            },

                            data: [{
                                    value: 10,
                                    name: 'A'
                                }, {
                                    value: 20,
                                    name: 'B'
                                },
                                {
                                    value: 40,
                                    name: 'C'
                                },
                                {
                                    value: 60,
                                    name: 'D'
                                },
                                {
                                    value: 80,
                                    name: 'E'
                                },
                                {
                                    value: 100,
                                    name: 'F'
                                }
                            ]
                        },
                        {
                            name: 'TIT',
                            type: 'funnel',
                            left: 'center',
                            width: '80%',
                            maxSize: '80%',
                            sort: 'ascending',
                            label: {
                                normal: {
                                    position: 'inside',
                                    formatter: '{c}%',
                                    textStyle: {
                                        color: '#fff',
                                        fontSize:14,
                                    }
                                },
                                emphasis: {
                                    position: 'inside',
                                    formatter: '{b}: {c}%'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    opacity: 0.8,
                                    borderColor: 'rgba(12, 13, 43, .9)',
                                    borderWidth: 3,
                                    shadowBlur: 5,
                                    shadowOffsetX: 0,
                                    shadowOffsetY: 5,
                                    shadowColor: 'rgba(0, 0, 0, .6)'
                                }
                            },
                            data: [{
                                    value: 2,
                                    name: 'A'
                                }, {
                                    value: 5,
                                    name: 'B'
                                },
                                {
                                    value: 12,
                                    name: 'C'
                                },
                                {
                                    value: 18,
                                    name: 'D'
                                },
                                {
                                    value: 25,
                                    name: 'E'
                                },
                                {
                                    value: 40,
                                    name: 'F'
                                }
                            ]
                        }
                    ]
                };
                myChart.setOption(option)
            },
            initEcharts1 () {
                const myChart = echarts.init(document.getElementById('timeLine'))
                var fontColor = '#fff';
                let option = {
                    color: ['#bf19ff', '#854cff', '#5f45ff', '#02cdff', '#0090ff', '#f9e264', '#f47a75', '#009db2', '#0780cf', '#765005'],
                    backgroundColor: '#0f375f',
                    textStyle: {
                        fontSize: 18
                    },
                    grid: {
                        left: '20',
                        right: '50',
                        bottom: '50',
                        top: '80',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow',
                            label: {
                                show: true,
                                backgroundColor: '#333'
                            }
                        }
                    },
                    legend: {
                        show: true,
                        x: 'center',
                        top: '20',
                        textStyle: {
                            color: fontColor
                        },
                        data: ['中央', '自治区', '盟市', '旗县区', '整合资金', '其他']
                    },
                    xAxis: [{
                        type: 'category',
                        boundaryGap: false,
                        axisLabel: {
                            color: fontColor
                        },
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: '#397cbc'
                            }
                        },
                        data: ['2016年', '2017年', '2018年', '2019年', '2020年']
                    }],
                    yAxis: [{
                        type: 'value',
                        name: '亿元',
                        axisLine: {
                            lineStyle: {
                                color: fontColor
                            }
                        }
                    }],
                    series: [{
                            name: '中央',
                            type: 'line',
                            stack: '总量',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,44,90,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0,146,246,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [120, 132, 101, 134, 90, 230, 210, 182, 191, 234, 260, 280]
                        },
                        {
                            name: '自治区',
                            type: 'line',
                            stack: '总量',
                            symbol: 'circle',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,44,90,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0,212,199,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [220, 182, 191, 210, 230, 270, 270, 201, 154, 140, 240, 250]
                        },
                        {
                            name: '盟市',
                            type: 'line',
                            stack: '总量',
                            symbol: 'circle',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,44,90,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(114,144,89,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [150, 232, 201, 154, 190, 180, 210, 150, 182, 201, 154, 190]
                        },
                        {
                            name: '旗县区',
                            type: 'line',
                            stack: '总量',
                            symbol: 'circle',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,46,101,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0,166,246,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [150, 232, 201, 154, 190, 180, 210, 150, 182, 201, 154, 190]
                        },
                        {
                            name: '整合资金',
                            type: 'line',
                            stack: '总量',
                            symbol: 'circle',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,44,90,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0,212,199,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [150, 232, 201, 154, 190, 180, 210, 150, 182, 201, 154, 190]
                        },
                        {
                            name: '其他',
                            type: 'line',
                            stack: '总量',
                            symbol: 'circle',
                            symbolSize: 8,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    areaStyle: {
                                        //color: '#94C9EC'
                                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: 'rgba(7,44,90,0.3)'
                                        }, {
                                            offset: 1,
                                            color: 'rgba(0,212,199,0.9)'
                                        }]),
                                    }
                                }
                            },
                            data: [200, 232, 201, 200, 190, 190, 210, 190, 182, 201, 154, 190]
                        }
                    ]
                };
                myChart.setOption(option)
            }
        }
    }
</script>
<style>

</style>