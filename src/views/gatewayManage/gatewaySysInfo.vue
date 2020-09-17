<template>
  <el-main class="no-padding sysinfo">
    <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>网关管理</el-breadcrumb-item>
        <el-breadcrumb-item>系统信息</el-breadcrumb-item>
    </el-breadcrumb>

    <el-container class="container_css">
      <el-aside class="aside_system" style="width: 4%;padding-top:85px;background-color: rgb(90, 170, 51);"><span>系统</span></el-aside>
      <el-container>
        <el-main>
          <el-progress id="cpu"  v-loading="loading" class="prog" type="dashboard" style="margin:2% 0px 2% 2%;" :percentage="cpu_status" :color="colors" :width="150" :height="150" ></el-progress>
          <span style="position: relative; right: 90px;margin-right:24px">CPU</span>
          <el-divider direction="vertical"></el-divider>

          <el-form v-loading="infoloading" :inline="true">
            <el-form-item label="主机名：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_hostname}}</span>
            </el-form-item>
            <el-form-item label="系统类型：">
              <span>基于X64的电脑</span>
            </el-form-item>
            <el-form-item label="产品名称：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_product_name}}</span>
            </el-form-item>
            <el-form-item label="操作系统：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_os}}</span>
            </el-form-item>
            <el-form-item label="RS232接口：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_rs232_num}}</span>
            </el-form-item>
            <el-form-item label="usb接口：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_usb_num}}</span>
            </el-form-item>
            <el-form-item label="当前使用端口：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_com}}</span>
            </el-form-item>
            <el-form-item label="usb接口使用数：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_use_usb_num}}</span>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </el-container>
    <el-container class="container_css">
      <el-aside class="aside_system" style="width: 4%;padding-top:85px;background-color: rgb(245, 108, 108)"><span>内存</span></el-aside>
      <el-container>
        <el-main>
          <el-progress class="prog" v-loading="loading" type="dashboard" style="margin:2% 0px 2% 2%;" :percentage="memory_status" :color="colors" :width="150" :height="150" ></el-progress>
          <span style="position: relative; right: 100px;">Memory</span>
          <el-divider direction="vertical"></el-divider>

          <el-form v-loading="infoloading" :inline="true" class="form_item">
            <el-form-item label="内存大小：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_memory}} G</span>
            </el-form-item>
            <el-form-item label="硬盘剩余：">
              <span v-for="(a,i) in systemData" :key="i">{{(Number(a.sys_harddisk_size) * (Number(a.sys_harddisk) * 0.01)).toFixed(2)}} G</span>
            </el-form-item>
            <el-form-item label="内存剩余：">
              <span v-for="(a,i) in systemData" :key="i">{{(Number(a.sys_memory) * (Number(a.sys_memory_size) * 0.01)).toFixed(2)}} G</span>
            </el-form-item>
            <el-form-item label="硬盘总量：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_harddisk_size}} G</span>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </el-container>
    <el-container class="container_css">
      <el-aside class="aside_system" style="width: 4%;padding-top:85px;background-color: rgb(230, 162, 60)"><span>网络</span></el-aside>
      <el-container>
        <el-main>
          <el-progress class="prog" v-loading="loading" type="dashboard" style="margin:2% 0px 2% 2%;" :percentage="disk_status" :color="colors" :width="150" :height="150" ></el-progress>
          <span style="position: relative; right: 90px;margin-right:27px">Disk</span>
          <el-divider direction="vertical"></el-divider>

          <el-form v-loading="infoloading" :inline="true" class="form_item">
            <el-form-item label="IP地址：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_ip}}</span>
            </el-form-item>
            <el-form-item label="MAC地址：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_mac}}</span>
            </el-form-item>
            <el-form-item label="子网掩码：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_mask}}</span>
            </el-form-item>
            <el-form-item label="本地时间：">
              <span v-for="(a,i) in systemData" :key="i">{{a.sys_local_time}}</span>
            </el-form-item>
            <el-form-item label="时区：">
              <span>中国标准时间</span>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </el-container>

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

<style>
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

<script>
// import system from "./components/System"
export default {
  data () {
    return {
      loading: true,
      infoloading: true,
      systemData: [],
      cpu_status: 0,
      memory_status: 0,
      disk_status: 0,
      colors: [
        { color: '#6f7ad3', percentage: 20 },
        { color: '#1989fa', percentage: 40 },
        { color: '#5cb87a', percentage: 60 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#f56c6c', percentage: 100 }
      ]
    }
  },
  // 初始化
  created () {
    this.getData()
    this.timer()
  },
  // components: {
  //   System
  // },
  destroyed () {
    clearInterval(this.positionTimer)// 清除定时器
    this.positionTimer = null
    // console.log('关闭定时器')
  },
  methods: {
    getData: function () {
      this.$axios.get('/apis/agent/sysinfo')
        .then(response => {
          this.systemData = response.data.results
          this.cpu_status = Number(this.systemData[0]['sys_rateof_cpu'])
          this.memory_status = Number(this.systemData[0]['sys_memory_size'])
          this.disk_status = Number(this.systemData[0]['sys_harddisk'])
          this.loading = false
          this.infoloading = false
        })
        .catch(error => {
          this.loading = true
          this.infoloading = true
          console.log(error)
        })
        
    },
    timer () {
      // console.log('开启定时器')
      // 这是一个定时器
      this.positionTimer = setInterval(() => {
        this.getData()
      }, 3000)
    }
  }
}
</script>

<style scoped>
</style>
