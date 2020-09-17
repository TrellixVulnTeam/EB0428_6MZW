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

      </el-tab-pane>
      <el-tab-pane label="本地MQTT服务" name="third">
        <!-- <el-button type="danger" @click="startmqtt()">开启MQTT</el-button> -->
        <el-table :data="mqtttableData">
          <el-table-column label="IP地址" prop="mqtthost"></el-table-column>
          <el-table-column label="端口号" prop="mqttport"></el-table-column>
          <el-table-column label="用户" prop="mqttusername"></el-table-column>
          <el-table-column label="密码" prop="mqttpassword"></el-table-column>
          <el-table-column label="运行状态">
            <template v-slot="scope">
              <el-tooltip placement="top">
                <div slot="content">开启或关闭MQTT服务器的通道</div>
                <el-switch v-model="scope.row.mqttstatus" @change="choosemqttStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="mqtt管理" >
            <template slot-scope="scope">
              <!-- <a :href="scope.row.mqtturl" target="_blank" class="buttonText">入口</a> -->
              <el-button type="text" style="color: #FF0000" @click="open_emq()">入口</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

    </el-tabs>

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
      tabIndex: 2,
      configmqttDialog: false, // 配置mqtt信息弹出框
      mqttForm: {  // mqtt信息
        host: '',
        port: '',
        username: '',
        password: ''
      },
      mqtttableData: [
        {
            mqtthost: '<N/A>',
            mqttport: '<N/A>',
            mqttusername: '<N/A>',
            mqttpassword: '<N/A>',
            mqttstatus: '<N/A>',
            mqtturl: '<N/A>'
        }
      ],
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
    },

    // mqtt启用或者禁用
    choosemqttStatus(row) {
      this.$axios.post("apis/agent/sysmqtt/", {
            enable: row.mqttstatus,
          }) 
        .then(response => {
          if(response.data.status_code==1){
            this.$Message.ErrorMessage(this, response.data.message);
          }
          else{
            this.$Message.SuccessMessage(this, response.data.message);
          }

        })
    },
    
    //打开emq管理页面
    open_emq() {
      
          // console.log('1111');
      if(this.mqtttableData[0]['mqttstatus']==false) {
        this.$Message.WarningAlert(this, "请先开启MQTT服务！");
      }
      else{
        window.open('http://localhost:18083/', "_blank")
        .then(function (response) {
          console.log(response.data.message);
          _this.flush_status()
        })
        .catch(function (error) {
          console.log(error);
        });
      };      
    },

  },
    // 初始化
  created () {
    
    this.$axios.get("apis/agent/sysmqtt/")
      .then(response => {
        this.mqtttableData = response.data.mqtt_data

    }) 
  }
};
</script>

<style scoped>
</style>
