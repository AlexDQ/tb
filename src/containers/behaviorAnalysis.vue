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
    import {mapState} from 'vuex'

    export default{
        data () {
            return {
            }
        },
        created () {
            this.$store.dispatch('location/GET_BUY_DATA')
            this.$store.dispatch('location/GET_TIME_DATA')
        },
        computed:{
            ...mapState({
                showFlag: state=> state.location.showFlag4,
                showFlag1: state=> state.location.showFlag5,
                buyXdata: state=> state.location.buyXdata,
                buyYdata: state=> state.location.buyYdata,
                buyData: state=> state.location.buyData,
                timeXdata: state=> state.location.timeXdata,
                timeYdata: state=> state.location.timeYdata
            })
        },
        mounted () {
            this.initEcharts()
            this.initEcharts1()
        },
        watch:{
            showFlag (newV, oldV) {
                if(newV){
                    this.initEcharts()
                }
            },
            showFlag1 (newV, oldV) {
                if(newV){
                    this.initEcharts1()
                }
            }
        },
        methods:{
            initEcharts () {
                const myChart = echarts.init(document.getElementById('loudou'))
                console.log(this.buyXdata, this.buyYdata, this.buyData)
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
                        data: this.buyXdata,
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

                            data: this.buyData
                        },
                        {
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
                            data:  this.buyData
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
                        data: this.timeXdata
                    }],
                    yAxis: [{
                        type: 'value',
                        name: '亿元',
                        axisLine: {
                            lineStyle: {
                                color: fontColor
                            }
                        },
                        data: this.timeYdata
                    }],
                    series: {
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
                            data: this.timeYdata
                        }
                };
                myChart.setOption(option)
            }
        }
    }
</script>
<style>

</style>