<template>
    <el-main>
        <!-- <el-button @click="updateTitle()">更改标题</el-button>
        <div :id="id" style="min-width: 600px;height:400px;"></div> -->
        <div id="pie" style="min-width: 600px;height:400px;"></div>
        <div id="line" style="min-width: 600px;height:400px;"></div>
    </el-main>
</template>

<script>
export default {
    data(){
        return{
            id: "bar",
            charts: null
        }
    },
    created(){
    },
    mounted(){
        // this.bar()
        this.pie()
        this.spline()
    },
    methods:{
        updateTitle(){
            //动态更新主标题
            const title = {
                //使用html语法
                useHTML: true,
                text: "更新后的标题<a href='http://127.0.0.1:8080'>重新加载页面</a>",
                style:{
                    color:"#ff0000"
                }
            }
            this.charts.setTitle(title)
            //动态更新副标题
            const subTitle = {
                text: "更新后的副标题",
                style:{
                    color: "#000",
                    fontWeight: "bold"
                }
            }
            this.charts.setTitle(null, subTitle)
        },
        activeLastPointToolip(chart) {
            let points = chart.series[0].points;
            chart.tooltip.refresh(points[points.length -1]);
        },
        bar(){
            let options = {
                chart: {
                    //指定图表的类型，默认是折线图（line）
                    //图表类型
                    type: 'bar', 
                    //指定容器
                    renderTo: "bar",
                    //指定缩放：x, y, xy
                    zoomType: "xy",
                    //平移键
                    pankey: "Shift",
                    //是否启用平移
                    panning: true
                },
                //标题
                title: {
                    //隐藏标题，设为空即可 
                    //text: null
                    text: '我的主标题'                 // 标题
                },
                //副标题
                subtitle:{
                    text: '我的副标题'
                },
                //x坐标轴
                xAxis: {
                    categories: ['苹果', '香蕉', '橙子']   // x 轴分类
                },
                //y坐标轴
                yAxis: {
                    title: {
                        text: '吃水果个数'                // y 轴标题
                    },
                    //自定义标签格式
                    labels: {
                        formatter:function(){
                            if(this.value <= 1){
                                return "aaa" + this.value
                            }else if(this.value > 1 && this.value <= 4){
                                return "bbb" + this.value
                            }else{
                                return "ccc" + this.value
                            }
                        }
                    }
                },
                //数据
                series: [{                              // 数据列
                    name: '小明',                        // 数据列名
                    data: [1, 0, 4]                     // 数据
                }, {
                    name: '小红',
                    data: [5, 7, 3]
                }],
                //样式
                style: {

                },
            };
            // var charts = this.$highCharts.chart(this.id, options)
            this.charts = this.$highCharts.chart(options)
        },
        pie(){
            const _this = this
            let options = {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    renderTo: "pie",
                    type: 'pie'
                },
                title: {
                        text: 'EdgeBox设备在线状态'
                },
                tooltip: {
                        pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                        pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                        enabled: true,
                                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                        style: {
                                                color: (_this.$highCharts.theme && _this.$highCharts.theme.contrastTextColor) || 'black'
                                        }
                                }
                        }
                },
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                                name: '在线设备',
                                y: 3,
                                sliced: true,
                                selected: true
                        }, {
                                name: '离线设备',
                                y: 5
                        }]
                }]
            }
            this.$highCharts.chart(options)
        },
        spline(){
            const _this = this
            let chart = this.$highCharts.chart({
                chart: {
                    type: 'spline',
                    renderTo: "line",
                    marginRight: 10,
                    events: {
                        load: function () {
                            let series = this.series[0],
                                chart = this;
                            _this.activeLastPointToolip(chart);
                            setInterval(() => {
                                let x = (new Date()).getTime(), // 当前时间
                                    y = Math.random() * 100;          // 随机值
                                series.addPoint([x, y], true, true);
                                _this.activeLastPointToolip(chart);
                            }, 1000);
                        }
                    }
                },
                title: {
                    text: '上行消息数'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150
                },
                yAxis: {
                    title: {
                        text: null
                    }
                },
                tooltip: {
                    formatter: function () {
                        return '<b>' + this.series.name + '</b><br/>' +
                            _this.$highCharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                            _this.$highCharts.numberFormat(this.y, 2);
                    }
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: '随机数据',
                    data: (function () {
                            // 生成随机值
                            let data = [],
                                    time = (new Date()).getTime(),
                                    i;
                            for (i = -19; i <= 0; i += 1) {
                                    data.push({
                                            // x: time + i * 1000,
                                            x: time,
                                            y: Math.random()
                                    });
                            }
                            return data;
                    }())
                }]
            });
        }
    }
}
</script>