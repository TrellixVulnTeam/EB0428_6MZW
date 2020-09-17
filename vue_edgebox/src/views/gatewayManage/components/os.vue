<template>
  <el-container>
          <el-main>
            <el-progress class="prog"
             v-loading="loading" 
             type="dashboard" 
             style="margin:2% 0px 2% 2%;" 
             :percentage="memory_status" 
             :color="colors" 
             :width="150" :height="150" ></el-progress>
            <span style="position: relative; right: 100px;">Memory</span>
            <el-divider direction="vertical"></el-divider>

            <el-form v-loading="infoloading" :inline="true" class="form_item">
              <el-form-item label="总内存(G)：">
                <span> {{systemData.total_nc}} </span>
              </el-form-item>
              <el-form-item label="已用内存(G):">
                <span> {{systemData.used_nc}} </span>
              </el-form-item>
              <el-form-item label="空闲内存(G):">
                <span> {{systemData.free_nc}} </span>
              </el-form-item>
              <el-form-item label="内存使用率(%):">
               <span> {{systemData.syl_nc}} </span>
              </el-form-item>
              <el-form-item label="路由网关:">
               <span> {{systemData.routingGateway}} </span>
              </el-form-item>
              <el-form-item label="子网掩码:">
               <span> {{systemData.routingIPNetmask}} </span>
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
          memory_status: 0,
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
        this.$axios.get("apis/agent/sysinfo?os=1")
        .then(response => {
          this.memory_status = response.data.memory_status;
          this.systemData = response.data.data_for_sys
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
