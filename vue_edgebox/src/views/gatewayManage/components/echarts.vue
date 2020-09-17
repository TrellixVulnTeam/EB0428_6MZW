<template>
    <el-main>
        <div id="bar" style="width:98%;height:20em"></div>
        <div id="line" style="width:98%;height:20em"></div>
        <div id="pie" style="width:98%;height:20em"></div>
        <div id="barPlus" style="width:98%;height:20em"></div>
    </el-main>
</template>
<style>
    #bar,#line,#pie,#barPlus{
        display: none;
    }
    #bar,#line,#pie,#barPlus div,canvas{
        width: 100%
    }
</style>
<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your ECharts'
    }
  },
  created(){
  },
  mounted(){
    // this.bar();
    // this.drawLine()
  },
  methods: {
    bar(){
        $("#bar").show()
        // 基于准备好的dom，初始化echarts实例
        //柱状图
        let bar = this.$echarts.init(document.getElementById("bar"))
        bar.setOption({
            title: { text: '柱状图' },
            tooltip: {},
            xAxis: {
                data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        });
        window.addEventListener("resize", function () {
            bar.resize();
        });
    },
    line(){
        $("#line").show()
        //折线图
        let line = this.$echarts.init(document.getElementById("line"))
        line.setOption({
            title: { text: '折线图' },
            tooltip: {},
            xAxis: { 
                type: 'category',
                data:  ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [{
				name: '数据',
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                type: 'line'
            }]
        });
        window.addEventListener("resize", function () {
            line.resize();
        });
    },
    pie(){
        $("#pie").show()
        //折线加饼图
        let pie = this.$echarts.init(document.getElementById("pie"))
        pie.setOption({
            title:{text: '折线加饼图'},
            legend: {},
            tooltip: {
                trigger: 'axis',
                showContent: false
            },
            dataset: {
                source: [
                    ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
                    ['Matcha Latte', 41.1, 30.4, 65.1, 53.3, 83.8, 98.7],
                    ['Milk Tea', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1],
                    ['Cheese Cocoa', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5],
                    ['Walnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
                ]
            },
            xAxis: {type: 'category'},
            yAxis: {gridIndex: 0},
            grid: {top: '55%'},
            series: [
                {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                {
                    type: 'pie',
                    id: 'pie',
                    radius: '30%',
                    center: ['50%', '25%'],
                    label: {
                        formatter: '{b}: {@2012} ({d}%)'
                    },
                    encode: {
                        itemName: 'product',
                        value: '2012',
                        tooltip: '2012'
                    }
                }
            ]
        })
        pie.on('updateAxisPointer', function (event) {
            var xAxisInfo = event.axesInfo[0];
            if (xAxisInfo) {
                var dimension = xAxisInfo.value + 1;
                pie.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                });
            }
        });
        window.addEventListener("resize", function () {
            pie.resize();
        });
    },
    barPlus(){
        $("#barPlus").show()//柱状图升级
        let barPlus = this.$echarts.init(document.getElementById("barPlus"))
        var dataCount = 1e3;//1e5 = 1*10的5次方
        var _this = this
        
        var data = generateData(dataCount);
        barPlus.setOption({
            title: {
                text: "柱状图升级:" + this.$echarts.format.addCommas(dataCount) + ' Data',
                left: 10
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: false
                    },
                    saveAsImage: {
                        pixelRatio: 2
                    }
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                bottom: 90
            },
            dataZoom: [{
                type: 'inside'
            }, {
                type: 'slider'
            }],
            xAxis: {
                data: data.categoryData,
                silent: false,
                splitLine: {
                    show: false
                },
                splitArea: {
                    show: false
                }
            },
            yAxis: {
                splitArea: {
                    show: false
                }
            },
            series: [{
                type: 'bar',
                data: data.valueData,
                // Set `large` for large data amount
                large: true
            }]
        })
        function generateData(count) {
            var baseValue = Math.random() * 1000;
            var time = +new Date(2019, 0, 1);
            var smallBaseValue;

            function next(idx) {
                smallBaseValue = idx % 30 === 0
                    ? Math.random() * 700
                    : (smallBaseValue + Math.random() * 500 - 250);
                baseValue += Math.random() * 20 - 10;
                return Math.max(
                    0,
                    Math.round(baseValue + smallBaseValue) + 3000
                );
            }

            var categoryData = [];
            var valueData = [];
            for (var i = 0; i < count; i++) {
                categoryData.push(_this.$echarts.format.formatTime('yyyy-MM-dd\nhh:mm:ss', time));
                valueData.push(next(i).toFixed(2));
                time += 1000;
            }

            return {
                categoryData: categoryData,
                valueData: valueData
            };
        }
        window.addEventListener("resize", function () {
            barPlus.resize();
        });
    },
    drawLine(){

    },
  }
}
</script>