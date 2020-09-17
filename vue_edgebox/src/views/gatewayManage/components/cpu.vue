<template>
  <el-container>
    <el-main>
        <el-progress id="cpu"  
        v-loading="loading" 
        class="prog" 
        type="dashboard" 
        style="margin:2% 0px 2% 2%;"
        :color="colors"
        :percentage="cpu_status" 
        :width="150" :height="150" ></el-progress>
        <span style="position: relative; right: 90px;margin-right:24px">CPU</span>
        <el-divider direction="vertical"></el-divider>
        <el-form v-loading="infoloading" :inline="true" class="form_item">
            <el-form-item label="用户时间(%):">
              <span> {{systemData.user_time}}</span>
            </el-form-item>
            <el-form-item label="系统时间(%):">
              <span> {{systemData.sys_time}}</span>
            </el-form-item>
            <el-form-item label="空闲时间(%):">
              <span> {{systemData.free_time}}</span>
            </el-form-item>
            <el-form-item label="逻辑CPU个数:">
              <span> {{systemData.core_num}}</span>
            </el-form-item>
             <el-form-item label="物理CPU个数:">
              <span> {{systemData.core_threads}}</span>
            </el-form-item>
             <el-form-item label="CPU使用情况:">
              <span> {{systemData.use_status}}</span>
            </el-form-item>
          </el-form>
        <!-- <el-form v-loading="infoloading" :inline="true">
            <el-form-item v-for="(item ,index) of fromData" :key="index" :label="item">
            </el-form-item>
        </el-form> -->
    </el-main>
    </el-container>
</template>

<script>
  export default {
    // 数据
    name: "CPU",
    data() {
      return {
          infoloading: false,
          loading: false,
          cpu_status: 0 ,
          systemData:{
            "sys_local_time":12
          },
        //   fromData: [
        //       ["用户时间(百分比)", "15:5656:415:131"],
        //       ["系统时间(百分比)", "15:5656:415:131"],
        //       ["空闲时间(百分比)", "15:5656:415:131"],
            //   ["核数", "15:5656:415:131"],
        //       ["逻辑CPU个数", "4"],
        //       ["物理CPU个数", "4"],
        //       ['CPU使用情况', [1,2,3,4]],
        //     ],
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
        this.loading =true;
        this.$axios.get("apis/agent/sysinfo?cpu=1")
        .then(response => {
          this.cpu_status = response.data.cpu_status;
          this.systemData = response.data.data_for_cpu
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
