<template>
  <el-main class="no-padding">
      <el-button @click="flush_status" type="primary" size="small" style="margin:20px" plain >
        点我立即刷新
      </el-button>
      <label for="cpu">
        <el-progress id="cpu" type="dashboard" :percentage="cpu_status" :color="colors"></el-progress>
      </label>
      <span style="position: relative; right: 82px">CPU</span>
      <el-progress type="dashboard" :percentage="memory_status" :color="colors" style="position: relative; left: 20px"></el-progress>
      <span style="position: relative; right: 75px">Memory</span>
      <el-progress type="dashboard" :percentage="disk_status" :color="colors" style="position: relative; left: 20px"></el-progress>
      <span style="position: relative; right: 60px">Disk</span>
      <!-- <el-card style="position: relative; right: 60px width:30%"  class="box-card"></el-card> -->
      <el-table
        :data="tableData6"
        border
        :summary-method="getSummaries"
        height="400"
        show-summary
        style="width: 100%; margin-top: 5px; height:40%">
        <el-table-column
        sortable
          prop="id"
          label="Time"
          width="180">
        </el-table-column>
        <el-table-column
        sortable
          prop="cpu"
          label="CPU使用(%)">
        </el-table-column>
        <el-table-column
        sortable
          prop="memory"
          label="内存使用(%)">
        </el-table-column>
        <el-table-column
        sortable
          prop="disk"
          label="磁盘使用(%)">
        </el-table-column>
        <el-table-column
        sortable
          prop="num"
          label="接口使用(个)">
        </el-table-column>
      </el-table>
  </el-main>
</template>

<script>
  export default {
    // 数据
    name: "System",
    data() {
      return {
        total: 100,
        tableData6: [{
          id: '2020/03/22 08:00:00.234',
          cpu: '65.3',
          memory: '54.4',
          disk: '28.5',
          num: 4
        },],
        colors: [
          {color: '#6f7ad3', percentage: 20},
          {color: '#1989fa', percentage: 40},
          {color: '#5cb87a', percentage: 60},
          {color: '#e6a23c', percentage: 80},
          {color: '#f56c6c', percentage: 100}
        ],
        cpu_status: 0,
        memory_status: 0,
        disk_status: 0,
        loading: false
      }
    },
    // 响应事件
    methods: {
      getSummaries(param) {
        const { columns, data } = param;
        const sums = [];
        columns.forEach((column, index) => {
          if (index === 0) {
            sums[index] = '平均值(过去一小时)';
            return;
          }
          const values = data.map(item => Number(item[column.property]));
          if (!values.every(value => isNaN(value))) {
            sums[index] = values.reduce((prev, curr) => {
              const value = Number(curr);
              if (!isNaN(value)) {
                return (prev + curr);
              } else {
                return prev;
              }
            }, 0);
            sums[index] = sums[index]/this.total 
            sums[index] = Math.round(sums[index]*100)/100
          } else {
            sums[index] = 'N/A';
          }
        });

        return sums;
      },
      getData() {
        this.$axios.get("apis/agent/sysinfo/")
        .then(response => {
          this.cpu_status = response.data.cpu_status;
          this.memory_status = response.data.memory_status;
          this.disk_status = response.data.disk_status;
          this.tableData6 = response.data.table;
          this.total = response.data.total;
        })
        this.loading = false;
      },
      flush_status: function () {
        this.$axios.get("apis/agent/sysinfo/")
          .then(response => {
            this.cpu_status = response.data.cpu_status;
            this.memory_status = response.data.memory_status;
            this.disk_status = response.data.disk_status;
            this.tableData6 = response.data.table;
            this.total = response.data.total;
          })
      }
    },
    // 初始化
    created () {
      this.getData()      
    }
  }
</script>

<style scoped>

</style>
