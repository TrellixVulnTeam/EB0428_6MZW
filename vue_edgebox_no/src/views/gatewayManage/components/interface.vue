<template>
  <el-container>
        <el-main>
            <el-progress class="prog" 
            v-loading="loading"
            type="dashboard" 
            style="margin:2% 0px 2% 2%;"
            :percentage="disk_status" 
            :color="colors" 
            :width="150" :height="150" ></el-progress>
            <span style="position: relative; right: 90px;margin-right:27px">Disk</span>
            <el-divider direction="vertical"></el-divider>

            <el-form v-loading="infoloading" :inline="true" class="form_item">
              <el-form-item label="Ip地址：">
                <span> {{systemData.sys_ip}}</span>
              </el-form-item>
              <el-form-item label="MAC地址：">
                <span> {{systemData.sys_mac}}</span>
              </el-form-item>
              <el-form-item label="磁盘使用(%)：">
                <span> {{systemData.sys_harddisk}}</span>
              </el-form-item>
              <el-form-item label="磁盘大小(G)：">
                <span> {{systemData.sys_harddisk_size}}</span>
              </el-form-item>
              <el-form-item label="USB接口连接:">
                <span> {{systemData.sys_use_usb_num}}</span>
              </el-form-item>
              <el-form-item label="串口:">
                <span> {{systemData.sys_com}}</span>
              </el-form-item>
            </el-form>
          </el-main>
        </el-container>
</template>

<script>
  export default {
    // 数据
    name: "CPU",
    data() {
      return {
          disk_status: 0,
          loading: false,
          systemData:[],
          colors: [
          {color: '#6f7ad3', percentage: 20},
          {color: '#1989fa', percentage: 40},
          {color: '#5cb87a', percentage: 60},
          {color: '#e6a23c', percentage: 80},
          {color: '#f56c6c', percentage: 100}
        ],
      }
    },
    // 响应事件
    methods: {
      getData() {
        this.loading = true;
        this.$axios.get("apis/agent/sysinfo?interface=1")
        .then(response => {
          this.disk_status = response.data.disk_status;
          this.systemData = response.data.data_for_disk;
        })
        this.loading = false;
      },
    },
    // 初始化
    created () {
      this.getData()      
    }
  }
</script>

<style scoped>

</style>
