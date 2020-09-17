<template>
    <el-main :style="{'padding':'0px','background':'#f2f7fb','height':'100%'}">
        <!-- <el-button @click="addRouter">新增路由</el-button>
        <el-button @click="deleteRoute">清空路由</el-button> -->
        <!-- <span @click="render">{{rv}}</span> -->
        <div style="background-color: #1b578c;width:100%;height:50px"></div>
            <!-- <div id="line" style="min-width: 600px;height:400px;"></div> -->
        <div style="width:100%;margin-top:20px">
            <div style="margin:0 auto;width:90%;height:300px;padding:20px 0px">
                <div id="echartLine" style="margin:0 auto;width:90%;height:100%"></div>
            </div>
        </div>
    </el-main>
</template>

<style scoped>

</style>

<script>
export default {
    data(){
        return{
            i:0,
            rv:''
        }
    },
    created(){
        
        this.$phone
    },
    mounted(){
        this.echartLine()
    },
    methods:{
        echartLine(){
            var echartsLine = this.$echarts.init(document.getElementById("echartLine"))
            var option = {
                title: {
                    text: '动态数据',
                    subtext: '纯属虚构'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#283b56'
                        }
                    }
                },
                legend: {
                    data:['下行消息', '上行消息']
                },
                toolbox: {
                    show: true,
                    feature: {
                        dataView: {readOnly: false},
                        restore: {},
                        saveAsImage: {}
                    }
                },
                dataZoom: {
                    show: false,
                    start: 0,
                    end: 100
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: true,
                        data: (function (){
                            var now = new Date();
                            var res = [];
                            var len = 10;
                            while (len--) {
                                res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                                now = new Date(now - 2000);
                            }
                            return res;
                        })()
                    },
                    {
                        type: 'category',
                        boundaryGap: true,
                        data: (function (){
                            var res = [];
                            var len = 10;
                            while (len--) {
                                res.push(10 - len - 1);
                            }
                            return res;
                        })()
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        scale: true,
                        name: '下行消息量',
                        max: 30,
                        min: 0,
                        boundaryGap: [0.2, 0.2]
                    },
                    {
                        type: 'value',
                        scale: true,
                        name: '上行消息量',
                        max: 1200,
                        min: 0,
                        boundaryGap: [0.2, 0.2]
                    }
                ],
                series: [
                    {
                        name: '下行消息',
                        type: 'bar',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        data: (function (){
                            var res = [];
                            var len = 10;
                            while (len--) {
                                res.push(Math.round(Math.random() * 1000));
                            }
                            return res;
                        })()
                    },
                    {
                        name: '上行消息',
                        type: 'line',
                        data: (function (){
                            var res = [];
                            var len = 0;
                            while (len < 10) {
                                res.push((Math.random()*10 + 5).toFixed(1) - 0);
                                len++;
                            }
                            return res;
                        })()
                    }
                ]
            }

            app.count = 11;
            setInterval(function (){
                var axisData = (new Date()).toLocaleTimeString().replace(/^\D*/, '');

                var data0 = option.series[0].data;
                var data1 = option.series[1].data;
                data0.shift();
                data0.push(Math.round(Math.random() * 1000));
                data1.shift();
                data1.push((Math.random() * 10 + 5).toFixed(1) - 0);

                option.xAxis[0].data.shift();
                option.xAxis[0].data.push(axisData);
                option.xAxis[1].data.shift();
                option.xAxis[1].data.push(app.count++);

                echartsLine.setOption(option);
            }, 2100);
            //根据窗口的大小变动图表 --- 重点
            window.onresize = function(){
                echartsLine.resize();
                //myChart1.resize();    //若有多个图表变动，可多写

            }
        },
        render(){
            window.open(this.rv)
        }
    }
}
</script>