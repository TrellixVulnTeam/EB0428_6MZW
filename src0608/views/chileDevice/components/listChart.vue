<template>
    <el-main :style="{'padding':'0px','background':'#f2f7fb','height':'100%'}">
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
        
        !function(e){
            function t(a){
                if(i[a])return i[a].exports;
                var n=i[a]={exports:{},id:a,loaded:!1};
                return e[a].call(n.exports,n,n.exports,t),n.loaded=!0,n.exports
            }
            var i={};
            return t.m=e,t.c=i,t.p="",t(0)
        }([function(e,t){
            "use strict";
            Object.defineProperty(t,"__esModule",{value:!0});
            var i=window;
            t["default"]=i.flex=function(normal,e,t){
                var a=e||100,
                    n=t||1,
                    r=i.document,
                    o=navigator.userAgent,
                    d=o.match(/Android[\S\s]+AppleWebkit\/(\d{3})/i),
                    l=o.match(/U3\/((\d+|\.){5,})/i),
                    c=l&&parseInt(l[1].split(".").join(""),10)>=80,
                    p=navigator.appVersion.match(/(iphone|ipad|ipod)/gi),
                    s=i.devicePixelRatio||1;p||d&&d[1]>534||c||(s=1);
                var u=normal?1:1/s,
                    m=r.querySelector('meta[name="viewport"]');
                m||(m=r.createElement("meta"),
                m.setAttribute("name","viewport"),
                r.head.appendChild(m)),
                m.setAttribute("content","width=device-width,user-scalable=no,initial-scale="+u+",maximum-scale="+u+",minimum-scale="+u),
                r.documentElement.style.fontSize=normal?"50px": a/2*s*n+"px"
            },e.exports=t["default"]
        }]);
        flex(false,20,1)
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
            window.onresize = function(){
                echartsLine.resize();

            }
        },
    }
}
</script>