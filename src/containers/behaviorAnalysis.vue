<template>
    <div id='behaviorAnalysis' style='padding:20px'>
        <div style='padding:20px;background:#fff;text-align: center;'>
            <h4 style='margin-bottom: 10px;'>
                购买行为习惯分析
            </h4> 
            <div id='loudou' style='width:100%;height:500px;'>

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
            }
        }
    }
</script>
<style>

</style>