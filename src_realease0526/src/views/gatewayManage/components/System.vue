<template>
    <div id = "System" v-loading="loading" class="row-padding">
      <el-card style="min-height: 200px; max-height: 500px; ">
        <div slot="header">
          仪表盘
          <!-- <el-button @click="flush_status" type="primary" size="small" plain >
            点我立即刷新
          </el-button> -->
        </div>

        <div>
          <el-progress id="cpu" class="prog" type="dashboard" :percentage="cpu_status" :color="colors"></el-progress>
          <span style="position: relative; right: 82px">CPU</span>
          <el-progress type="dashboard" class="prog" :percentage="memory_status" :color="colors" style="position: relative; left: 20px"></el-progress>
          <span style="position: relative; right: 75px">Memory</span>
          <el-progress type="dashboard" class="prog" :percentage="disk_status" :color="colors" style="position: relative; left: 20px"></el-progress>
          <span style="position: relative; right: 60px">Disk</span>
        </div>
      </el-card>
    </div>
</template>
<style scoped>
  /* .prog{
    position: relative;
    left: 20%;
  } */
</style>
<script>
export default {
  // 数据
  name: 'System',
  data () {
    return {
      colors: [
        { color: '#6f7ad3', percentage: 20 },
        { color: '#1989fa', percentage: 40 },
        { color: '#5cb87a', percentage: 60 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#f56c6c', percentage: 100 }
      ],
      cpu_status: 0,
      memory_status: 0,
      disk_status: 0,
      loading: false
    }
  },
  destroyed () {
    clearInterval(this.positionTimer)// 清除定时器
    this.positionTimer = null
    console.log('关闭定时器')
  },
  // 响应事件
  methods: {
    flush_status: function () {
      // this.$axios.get("apis/agent/sysinfo/")
      //   .then(response => {
      //     this.cpu_status = response.data.cpu_status;
      //     this.memory_status = response.data.memory_status;
      //     this.disk_status = response.data.disk_status;
      //   })
      this.$axios.get('/wangguang/database')
        .then(response => {
          this.cpu_status = (response.data.results[0])['sys_rateof_cpu']
          this.memory_status = (response.data.results[0])['sys_memory_size']
          this.disk_status = (response.data.results[0])['sys_harddisk']
        })
    },
    timer () {
      console.log('开启定时器')
      // 这是一个定时器
      this.positionTimer = setInterval(() => {
        this.flush_status()
      }, 2000)
    }
  },
  // 初始化
  created () {
    this.loading = false
    this.timer()
  }
}
</script>

<style scoped>

</style>
