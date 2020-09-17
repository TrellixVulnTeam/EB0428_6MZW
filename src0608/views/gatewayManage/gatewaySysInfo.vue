<template>
  <el-main class="no-padding sysinfo">
    <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>网关管理</el-breadcrumb-item>
        <el-breadcrumb-item>系统信息</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row >
      <el-tabs v-model="activeName" type="border-card" class="tabs-margin-top" >
        <el-tab-pane label="全部" name= '0' style="overflow-y:auto;overflow-x:hidden;">
            <system v-if="activeName === '0'"></system>
            <!-- <el-button style="float: left"></el-button> -->
            
        </el-tab-pane>  
     
        <el-tab-pane label="CPU" name= '1' style="overflow-y:auto;overflow-x:hidden;">
          <cpu  v-if="activeName === '1'" ></cpu>
        </el-tab-pane>
        <el-tab-pane label="系统" name= '2' style="overflow-y:auto;overflow-x:hidden;">
          <os  v-if="activeName === '2'" ></os>
        </el-tab-pane>
        <el-tab-pane  label="硬件接口" name= '3' style="overflow-y:auto;overflow-x:hidden;">
          <interFace  v-if="activeName === '3'" ></interFace>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    

    <!-- <div id="info" v-loading="infoloading">
      <el-table :data="systemData" border>
        <el-table-column label="计算机名称" prop="sys_hostname"></el-table-column>
        <el-table-column label="产品名称" prop="sys_product_name"></el-table-column>
        <el-table-column label="系统运行环境" prop="sys_os"></el-table-column>
        <el-table-column label="网络状态" prop="sys_net_status"></el-table-column>
      </el-table>
      <el-table :data="systemData"  border>
        <el-table-column label="MAC地址" prop="sys_mac"></el-table-column>
        <el-table-column label="IP地址" prop="sys_ip"></el-table-column>
        <el-table-column label="子网掩码" prop="sys_mask"></el-table-column>
        <el-table-column label="默认网关" prop="sys_gateway"></el-table-column>
      </el-table>
      <el-table :data="systemData"  border>
        <el-table-column label="usb接口" prop="sys_usb_num"></el-table-column>
        <el-table-column label="rs232接口" prop="sys_rs232_num"></el-table-column>
        <el-table-column label="网络模块" prop="sys_net_model"></el-table-column>
      </el-table>
      <el-table :data="systemData"  border>
        <el-table-column label="系统运行时间" prop="sys_running_time"></el-table-column>
        <el-table-column label="系统本地时间" prop="sys_local_time"></el-table-column>
        <el-table-column label="系统出厂时间" prop="sys_out_time"></el-table-column>
      </el-table>
    </div> -->
  </el-main>
</template>


<script>
import system from "./components/System"
import cpu from "./components/cpu"
import os from "./components/os"
import interFace from "./components/interface"

export default {
  data () {
    return {
      loading: false,
      systemData: [],
      cpu_status: 0,
      memory_status: 0,
      disk_status: 0,
      activeName: '0',
      colors: [
        { color: '#6f7ad3', percentage: 20 },
        { color: '#1989fa', percentage: 40 },
        { color: '#5cb87a', percentage: 60 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#f56c6c', percentage: 100 }
      ],
      
    }
  },
  // 初始化
  created () {
    // this.getData()
    // this.timer()
  },
  // components: {
  //   System
  // },
  destroyed () {
    // clearInterval(this.positionTimer)// 清除定时器
    // this.positionTimer = null
    // console.log('关闭定时器')
  },
  methods: {
    
    timer () {
      // console.log('开启定时器')
      // 这是一个定时器
      this.positionTimer = setInterval(() => {
        this.getData()
      }, 3000)
    }
  },
  components: {
    system,
    cpu,
    os,
    interFace
  }
}
</script>


<style scope>
  .el-table__footer-wrapper tbody td, .el-table__header-wrapper tbody td {
    background-color: #23b15c;
    color: #f5f7fa;
  }
  .sysinfo .el-form{
    width: 71%;
    float: right;
  }
  .sysinfo .form_item{
    margin-top: 0.5em;
  }
  .sysinfo .form_item .el-form-item{
    margin: 0.5em 0px 0.5em 0px;
  }
  .sysinfo .el-form-item{
    margin-bottom: 0.4em;
  }
  .sysinfo .el-form-item__label{
    width: 8.5em;
  }
  .sysinfo .el-form-item__content{
    margin-left: 1em;
    width: 14em;
  }
  .sysinfo .el-divider--vertical{
    height: 100%;
    vertical-align: top;
  }
  .sysinfo .el-progress-circle{
    width: 100%;
    height: 100%;
  }
  .sysinfo .container_css{
    margin: 2% 0px 1% 1%;
    width: 98%;
    box-shadow: rgb(163, 160, 160) -3px -3px 10px;
    border-radius: 10px;
  }
  .sysinfo .aside_system{
      color: white;
      font-size: 1.5em;
      text-align: center;
      border-radius: 10px 0px 0px 10px;
    }
  /* .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  .el-container {
    margin-bottom: 40px;
  } */
</style>