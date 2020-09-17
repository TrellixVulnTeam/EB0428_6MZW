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
              <a :href="scope.row.mqtturl" target="_blank" class="buttonText">入口</a>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

    </el-tabs>



        <!-- 配置mqtt弹出框 -->
    <el-dialog title="配置mqtt" :visible.sync="configmqttDialog" custom-class="chile-device-box dialog-form"  width="560px">
      <el-form :model="mqttForm" label-position="left" label-width="100px">
        
        <el-form-item label="IP地址:" prop="host">
          <el-input type="text" size="small" v-model="mqttForm.host" placeholder="127.0.0.1" disabled></el-input>
        </el-form-item>
        <el-form-item label="端口号:" prop="port">
          <el-input type="text" size="small" v-model="mqttForm.port" placeholder="1883" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户名:" >
          <el-input type="text" size="small" v-model="mqttForm.username" placeholder="mqtt username :case admin"></el-input>
        </el-form-item>       
        <el-form-item label="密码:" >
          <el-input type="text" size="small" v-model="mqttForm.password" placeholder="mqtt password :case public"></el-input>
        </el-form-item>
        
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="resetmqttForm('mqttForm')">重置</el-button>
        <el-button type="primary" size="small" @click="submitmqttForm('mqttForm')">确定</el-button>
      </el-row>
    </el-dialog>

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
    startmqtt () {
      this.$confirm('即将开启本地MQTT服务！是否确定?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {

        this.$message({
          type: 'success',
          message: 'MQTT服务开启成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消MQTT服务开启!'
        })
      })
    },
    submitmqttForm(formName) {
      var _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/agent/info/', {
            params: this.form 
          }).then(response => {
            if(response.data.status_code === 0){
                this.$Message.SuccessMessage(this, response.data.message);
            }
            else{
              this.$Message.ErrorMessage(this, response.data.error);
            }
            this.dialogFormEdit = false;
            _this.resetForm(formName);
            _this.getData()
          })
          .catch(function (error) {
            console.log(error);
          });
        } else {
          console.log('error submit!!');
          return false;
        }
        });
    },
      resetmqttForm(formName) {
         this.$refs[formName].resetFields();
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
    // getmqttData(){
    //   this.$axios.get("apis/agent/sysmqtt/")
    //     .then(response => {
    //       this.enable = response.data.enable

      
    //   })  
    // },
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
