<template>
    <div id='dataAnalysis'>
        <div class='charts_wrapper'>
            <h4>每日PV访问量分析</h4>
            <div id='dataLine' style='width:100%;height:400px;margin-top:10px'>
            </div>
        </div>
        <div class='charts_wrapper'>
            <h4>每日UV</h4>
            <div id='UVline' style='width:100%;height:400px;margin-top:10px'>
            </div>
        </div>
        <div class='charts_wrapper'>
            <h4>客户总数分析</h4>
            <div id='totalBar' style='width:100%;height:400px;margin-top:10px'>
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
        this.initEcharts2()
    },  
    methods:{
        initEcharts () {
            const myChart = echarts.init(document.getElementById('dataLine'))
            let option = {
                backgroundColor: '#232d36',
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        lineStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0,
                                    color: 'rgba(0, 255, 233,0)'
                                }, {
                                    offset: 0.5,
                                    color: 'rgba(255, 255, 255,1)',
                                }, {
                                    offset: 1,
                                    color: 'rgba(0, 255, 233,0)'
                                }],
                                global: false
                            }
                        },
                    },
                },
                grid: {
                    top: '15%',
                    left: '10%',
                    right: '5%',
                    bottom: '15%',
                    // containLabel: true
                },
                xAxis: [{
                    type: 'category',
                    axisLine: {
                        show: false,
                        color: '#A582EA'
                    },

                    axisLabel: {
                        color: '#A582EA',
                        width: 100
                    },
                    splitLine: {
                        show: false
                    },
                    boundaryGap: false,
                    data: ["2020-06-21", "2020-06-22", "2020-06-23", "2020-06-24", "2020-06-25", "2020-06-26", "2020-06-27"] //this.$moment(data.times).format("HH-mm") ,

                }],

                yAxis: [{
                    type: 'value',
                    min: 0,
                    // max: 140,
                    splitNumber: 4,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#00BFF3',
                            opacity: 0.23
                        }
                    },
                    axisLine: {
                        show: false,
                    },
                    axisLabel: {
                        show: true,
                        margin: 20,
                        textStyle: {
                            color: '#fff',

                        },
                    },
                    axisTick: {
                        show: false,
                    },
                }],
                series: [{
                        name: '液压异常报警',
                        type: 'line',
                        showAllSymbol: true,
                        symbol: 'circle',
                        symbolSize: 10,
                        lineStyle: {
                            normal: {
                                color: "#A582EA",
                            },
                        },
                        label: {
                            show: true,
                            position: 'top',
                            textStyle: {
                                color: '#A582EA',
                            }
                        },
                        itemStyle: {
                            color: "#fff",
                            borderColor: "#A582EA",
                            borderWidth: 2,
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: 'rgba(43,193,145,0.3)'
                                    },
                                    {
                                        offset: 1,
                                        color: 'rgba(43,193,145,0)'
                                    }
                                ], false),
                            }
                        },
                        data: [4, 7, 5, 4, 3, 5, 8] //data.values
                    },
                    {
                        name: '液位异常报警',
                        type: 'line',
                        showAllSymbol: true,
                        symbol: 'circle',
                        symbolSize: 10,
                        lineStyle: {
                            normal: {
                                color: "#2CABE3",
                            },
                        },
                        label: {
                            show: true,
                            position: 'top',
                            textStyle: {
                                color: '#2CABE3',
                            }
                        },
                        itemStyle: {
                            color: "#fff",
                            borderColor: "#2CABE3",
                            borderWidth: 2,
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: 'rgba(81,150,164,0.3)'
                                    },
                                    {
                                        offset: 1,
                                        color: 'rgba(81,150,164,0)'
                                    }
                                ], false),
                            }
                        },
                        data: [3, 5, 4, 2, 1, 7, 6] //data.values
                    },
                ]
            };
            myChart.setOption(option)
        },
        initEcharts1 () {
            const myChart = echarts.init(document.getElementById('UVline'))
            const CubeLeft = echarts.graphic.extendShape({
                shape: {
                    x: 0,
                    y: 0
                },
                buildPath: function(ctx, shape) {
                    const xAxisPoint = shape.xAxisPoint
                    const c0 = [shape.x, shape.y]
                    const c1 = [shape.x - 9, shape.y - 9]
                    const c2 = [xAxisPoint[0] - 9, xAxisPoint[1] - 9]
                    const c3 = [xAxisPoint[0], xAxisPoint[1]]
                    ctx.moveTo(c0[0], c0[1]).lineTo(c1[0], c1[1]).lineTo(c2[0], c2[1]).lineTo(c3[0], c3[1]).closePath()
                }
            })
            const CubeRight = echarts.graphic.extendShape({
                shape: { 
                    x: 0,
                    y: 0
                },
                buildPath: function(ctx, shape) {
                    const xAxisPoint = shape.xAxisPoint
                    const c1 = [shape.x, shape.y]
                    const c2 = [xAxisPoint[0], xAxisPoint[1]]
                    const c3 = [xAxisPoint[0] + 18, xAxisPoint[1] - 9]
                    const c4 = [shape.x + 18, shape.y - 9]
                    ctx.moveTo(c1[0], c1[1]).lineTo(c2[0], c2[1]).lineTo(c3[0], c3[1]).lineTo(c4[0], c4[1]).closePath()
                }
            })
            const CubeTop = echarts.graphic.extendShape({
                shape: {
                    x: 0,
                    y: 0
                },
                buildPath: function(ctx, shape) {
                    const c1 = [shape.x, shape.y]
                    const c2 = [shape.x + 18, shape.y - 9]
                    const c3 = [shape.x + 9, shape.y - 18]
                    const c4 = [shape.x - 9, shape.y - 9]
                    ctx.moveTo(c1[0], c1[1]).lineTo(c2[0], c2[1]).lineTo(c3[0], c3[1]).lineTo(c4[0], c4[1]).closePath()
                }
            })
            echarts.graphic.registerShape('CubeLeft', CubeLeft)
            echarts.graphic.registerShape('CubeRight', CubeRight)
            echarts.graphic.registerShape('CubeTop', CubeTop)
            const MAX = [6000, 6000, 6000, 6000, 6000, 5000, 4000, 3000, 2000, 4000, 3000, 2000]
            const VALUE = [2012, 1230, 3790, 2349, 1654, 1230, 3790, 2349, 1654, 3790, 2349, 1654]
            let option = {
                backgroundColor: "#010d3a",
                title: {
                    text: '',
                    top: 32,
                    left: 18,
                    textStyle: {
                        color: '#00F6FF',
                        fontSize: 24
                    }
                },
                grid: {
                    left: 20,
                    right: 40,
                    bottom: '19%',
                    top: 107,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: ['德州', '德城区', '陵城区', '禹城市', '乐陵市', '临邑县',
                        '平原县', '夏津县', '武城县', '庆云县', '宁津县', '齐河县'
                    ],
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: 'white'
                        }
                    },
                    offset: 20,
                    axisTick: {
                        show: false,
                        length: 9,
                        alignWithLabel: true,
                        lineStyle: {
                            color: '#7DFFFD'
                        }
                    },
                    axisLabel: {
                        fontSize: 10
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: 'white'
                        }
                    },
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        fontSize: 16
                    },
                    boundaryGap: ['20%', '20%']
                },
                series: [{
                    type: 'custom',
                    renderItem: function(params, api) {
                        const location = api.coord([api.value(0), api.value(1)])
                        return {
                            type: 'group',
                            children: [{
                                type: 'CubeLeft',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: 'rgba(7,29,97,.6)'
                                }
                            }, {
                                type: 'CubeRight',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: 'rgba(10,35,108,.7)'
                                }
                            }, {
                                type: 'CubeTop',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: 'rgba(11,42,106,.8)'
                                }
                            }]
                        }
                    },
                    data: MAX
                }, {
                    type: 'custom',
                    renderItem: (params, api) => {
                        const location = api.coord([api.value(0), api.value(1)])
                        return {
                            type: 'group',
                            children: [{
                                type: 'CubeLeft',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: '#3B80E2'
                                        },
                                        {
                                            offset: 1,
                                            color: '#49BEE5'
                                        }
                                    ])
                                }
                            }, {
                                type: 'CubeRight',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: '#3B80E2'
                                        },
                                        {
                                            offset: 1,
                                            color: '#49BEE5'
                                        }
                                    ])
                                }
                            }, {
                                type: 'CubeTop',
                                shape: {
                                    api,
                                    xValue: api.value(0),
                                    yValue: api.value(1),
                                    x: location[0],
                                    y: location[1],
                                    xAxisPoint: api.coord([api.value(0), 0])
                                },
                                style: {
                                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: '#3B80E2'
                                        },
                                        {
                                            offset: 1,
                                            color: '#49BEE5'
                                        }
                                    ])
                                }
                            }]
                        }
                    },
                    data: VALUE
                }, {
                    type: 'bar',
                    label: {
                        normal: {
                            show: true,
                            position: 'top',
                            formatter: (e) => {
                                switch (e.name) {
                                    case '10kV线路':
                                        return VALUE[0]
                                    case '公用配变':
                                        return VALUE[1]
                                    case '35kV主变':
                                        return VALUE[2]
                                    case '水':

                                }
                            },
                            fontSize: 16,
                            color: '#fff',
                            offset: [4, -25]
                        }
                    },
                    itemStyle: {
                        color: 'transparent'
                    },
                    data: MAX
                }]
            }
            myChart.setOption(option)
        },
        initEcharts2 () {
            const myChart = echarts.init(document.getElementById('totalBar'))
            let option = {
                graphic: {
                    elements: [{
                        type: 'group',
                        left: 'center',
                        top: 'center',
                        children: [{
                                type: 'text',
                                left: 'center',
                                top: '0',
                                style: {
                                    text: 999,
                                    fontSize: 30,
                                    fill: '#0af'
                                }
                            },
                            {
                                type: 'text',
                                left: 'center',
                                top: '30',
                                style: {
                                    text: ' title',
                                    fontSize: 20,
                                }
                            }
                        ]
                    }]
                },
                grid: {
                    left: 3,
                    top: 45,
                    bottom: 0,
                    right: 0,
                    containLabel: true
                },
                xAxis: [{
                    // type: 'value',
                    data: ['x1', 'x2', 'x3', 'x4', 'x5'],
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false,
                        inside: true
                    },
                    axisLabel: {
                        // inside: true
                    },
                }],
                yAxis: [{
                    // type: 'category',
                    // data: ['y1', 'y2', 'y3', 'y4', 'y5'],
                    axisLine: {
                        show: false
                    },
                    splitLine: {
                        // show: false,
                        lineStyle: {
                            type: ['solid', 'dashed', 'dotted'][2]
                        }
                    },
                    axisTick: {
                        show: false,
                        inside: true
                    },
                    axisLabel: {
                        // inside: true,
                        // rotate: 45,
                        margin: 5,
                        formatter: function f(value, index) {
                            if (isNaN(value)) {
                                return value
                            }
                            value = +value
                            for (var i = 0; true; i++) {
                                var v = value / 10000;
                                if (v < 1) break;
                                value = v;
                            }
                            return (+value.toFixed(1)) +
                                Array(i % 2 + 1).join('万') +
                                Array(parseInt(i / 2) + 1).join('亿')
                        }
                    },
                }],
                dataZoom: [{
                    type: 'slider',
                    show: false,
                    start: 0,
                    end: 100
                }],
                tooltip: {
                    trigger: 'item'
                },
                tooltip: {
                    trigger: ['item', 'axis'][1],
                    position: function(pt) {
                        return [pt[0] - 14, '0'];
                    },
                    confine: true,
                    axisPointer: {
                        // type: 'cross',
                    },
                    extraCssText: 'transition:none;box-shadow:1px 1px 10px #aaa;background:rgba(0,0,0,.5);bottom:auto;top:0;margin-bottom:-30px;pointer-events:none',
                },
                color: ['#0af', '#21D100', '#FFD013', '#FF6767'],
                legend: {
                    right: 0,
                    icon: "rect",
                    itemGap: 16,
                    itemHeight: 8,
                    itemWidth: 20,
                    data: ['A', 'B', 'C'],
                    selected: {
                        'A': true,
                    }
                },
                series: [{
                    name: 'A',
                    type: ['line', 'bar', 'pie'][0],
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    },
                    z: 3,
                    data: [1, 2, 4, 4, 6, {
                        name: 'x',
                        value: 9
                    }]
                }, {
                    name: 'B',
                    type: ['line', 'bar', 'pie'][1],
                    barMaxWidth: 30,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    },
                    z: 2,
                    data: [5, 4, 2, 1, 1]
                }, {
                    name: 'C',
                    type: ['line', 'bar', 'pie'][2],
                    barMaxWidth: 30,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    },
                    radius: ['40%', '55%'],
                    z: 1,
                    label: {
                        align: 'left',
                        formatter: '{d}%  {c}\n{b}',
                    },
                    data: [{
                        name: '准点人数',
                        value: 17,
                    }, {
                        name: '迟到人数',
                        value: 1,
                    }, {
                        name: '请假人数',
                        value: 1,
                    }, {
                        name: '未打卡人数',
                        value: 1,
                    }]
                }]
            };
            myChart.setOption(option)

        }
    }
}
</script>
<style>

</style>