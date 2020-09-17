<template>
  <el-main class="no-padding">

    <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>网关管理</el-breadcrumb-item>
        <el-breadcrumb-item>网关服务</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 标签页 -->
    <el-tabs v-model="activeName" type="border-card" class="tabs-margin-top">
      <el-tab-pane label="重新启动" name="first">
        <el-button type="danger" @click="restartDev()">重新启动</el-button>
        <!-- 动态添加删除标签页 -->
        <!-- <div style="margin-bottom: 20px;margin-top: 20px;">
          <el-button
            size="small"
            @click="addTab(editableTabsValue)"
          >
            add tab
          </el-button>
        </div> -->
        <!-- <el-tabs v-model="editableTabsValue" type="border-card" closable @tab-remove="removeTab">
          <el-tab-pane
            v-for="(item) in editableTabs"
            :key="item.name"
            :label="item.title"
            :name="item.name"
          >
            {{item.content}}
          </el-tab-pane>
        </el-tabs> -->
      </el-tab-pane>
      <el-tab-pane label="恢复出厂设置" name="second">
        <el-button type="danger" @click="restore()">恢复出厂设置</el-button>
        <!-- <el-tabs v-model="activeName1" type="border-card" class="tabs-margin-top">
          <el-tab-pane label="重新启动" name="first">重新启动</el-tab-pane>
          <el-tab-pane label="恢复出厂设置" name="second">恢复出厂设置</el-tab-pane>
        </el-tabs> -->
      </el-tab-pane>
            <el-tab-pane label="开启MQTT服务" name="third">
          <el-button type="danger" @click="configmqtt()">配置MQTT</el-button>
      </el-tab-pane>
    </el-tabs>

    <!-- <el-row>
      <el-col :xl="12" :lg="12" :sm="24" :md="12">
        <highchart></highchart>
      </el-col>
    </el-row>
    <div>
      <div id="circleCenter" ref="chart" style="width:800px;height:300px" ></div>
      <div class="highcharts-container"></div>
    </div> -->
  </el-main>
</template>

<script>
export default {
  data () {
    return {
      activeName: 'second',
      activeName1: 'first',
      editableTabsValue: '2',
      editableTabs: [{
        title: 'Tab 1',
        name: '1',
        content: 'Tab 1 content'
      }, {
        title: 'Tab 2',
        name: '2',
        content: 'Tab 2 content'
      }],
      tabIndex: 2
    }
  },
  mounted () {
    this.draw()
  },
  methods: {
    draw () {
      let bar_dv = this.$refs.chart
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(bar_dv)
      // 绘制图表
      myChart.setOption(
        {
          color: ['#3398DB'],
          tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: ['7月1日', '7月2日', '7月3日', '7月4日', '7月5日', '7月6日', '7月7日', '7月8日', '7月9日'],
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '直接访问',
              type: 'bar',
              barWidth: '10%',
              data: [10, 52, 200, 334, 390, 330, 220, 300, 800]
            }
          ],
          plotOptions: {
            column: {
              colorByPoint: true
            }
          }
        }
      )
    },
    addTab (targetName) {
      let newTabName = ++this.tabIndex + ''
      this.editableTabs.push({
        title: 'New Tab',
        name: newTabName,
        content: 'New Tab content'
      })
      this.editableTabsValue = newTabName
    },
    removeTab (targetName) {
      let tabs = this.editableTabs
      let activeName = this.editableTabsValue
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabs[index + 1] || tabs[index - 1]
            if (nextTab) {
              activeName = nextTab.name
            }
          }
        })
      }

      this.editableTabsValue = activeName
      this.editableTabs = tabs.filter(tab => tab.name !== targetName)
    },
    restartDev () {
      this.$confirm('重新启动即为重启程序，程序一旦重启数据采集将会中断，网页将跳转至登录页面，请谨慎操作！是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        this.$message({
          type: 'success',
          message: '设备重启成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '设备重启已取消'
        })
      })
    },
    restore () {
      this.$confirm('恢复出厂设置将会清除您的所有配置信息，需要您重新配置，请谨慎操作！是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        this.$message({
          type: 'success',
          message: '设备恢复出厂设置成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消设备恢复出厂设置!'
        })
      })
    }
  }
}
</script>

<style scoped>
</style>
