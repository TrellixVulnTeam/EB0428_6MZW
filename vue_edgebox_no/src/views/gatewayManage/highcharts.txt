<template>
  <div>
    <x-chart id="highcharts" class="high" :option="option"></x-chart>
    <x-chart id="high" class="high" :option="option1"></x-chart>
  </div>
</template>
<style scoped>
 .high{
    width: 1000px;
    height: 500px;
    margin: 40px auto;
}
</style>
<script>
// 导入chart组件
import XChart from './charts'
var myvue = {}
export default {
  data () {
    return {
      option: {
      },
      data: [{
        name: '安装，实施人员',
        data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
      }, {
        name: '工人',
        data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
      }, {
        name: '销售',
        data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
      }, {
        name: '项目开发',
        data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
      }, {
        name: '其他',
        data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
      }],
      other: {
        title: {
          // 大标题
          text: ''
        },
        subtitle: {
          // 小标题
          text: ''
        },
        yAxis: {
          title: {
            text: ''
          }
        },
        xAxis: {
          title: {
            text: ''
          }
        },
        legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'middle'
        },
        plotOptions: {
          series: {
            dataLabels: {
              enabled: true,
              format: '{x} 年 \t {y} k'
              // formatter:function(){
              //     return this.x + "\t" + this.y + " mm";
              // }
            },
            allowPointSelect: true,
            label: {
              connectorAllowed: false
            },
            pointStart: 2010
          }
        },
        series: '',
        responsive: {
          rules: [{
            condition: {
              maxWidth: 500
            },
            chartOptions: {
              legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom'
              }
            }
          }]
        }
      },
      option1: {
        chart: {
          type: 'column'
        },
        title: {
          text: '月平均降雨量'
        },
        subtitle: {
          text: '数据来源: WorldClimate.com'
        },
        xAxis: {
          categories: [
            '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'
          ],
          crosshair: true
        },
        yAxis: {
          min: 0,
          title: {
            text: '降雨量 (mm)'
          }
        },
        tooltip: {
          // head + 每个 point + footer 拼接成完整的 table
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {
          column: {
            borderWidth: 0,
            colorByPoint: true
          },
          series: {
            allowPointSelect: true,
            dataLabels: {
              enabled: true,
              format: '{x} \t {y} mm'
              // formatter:function(){
              //     return this.x + "\t" + this.y + " mm";
              // }
            }
          }
        },
        series: [{
          type: 'line',
          name: '东京',
          data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 500, 194.1, 95.6, 54.4]
        }, {
          type: 'spline',
          name: '巴黎',
          data: [39.9, 11.5, 156.4, 119.2, 134.0, 146.0, 125.6, 138.5, 200, 494.1, 25.6, 44.4]
        }, {
          type: 'column',
          name: '华盛顿',
          data: [41.9, 73.5, 206.4, 229.2, 134.0, 116.0, 335.6, 448.5, 500, 294.1, 23.6, 44.4]
        }, {
          name: '北京',
          data: [139.9, 271.5, 306.4, 159.2, 154.0, 376.0, 235.6, 548.5, 100, 394.1, 195.6, 154.4]
        }]
      }
    }
  },
  beforeCreate: function () {
    myvue = this
  },
  mounted: function () {
    myvue.other.title.text = '2010 ~ 2016 年太阳能行业就业人员发展情况'
    myvue.other.subtitle.text = '数据来源：thesolarfoundation.com'
    myvue.other.series = myvue.data     // 数据
    myvue.other.yAxis.title.text = '就业人数'   // 数据
    myvue.other.xAxis.title.text = '年份'   // 数据
    myvue.option = myvue.other
  },
  components: {
    XChart
  }
}
</script>
