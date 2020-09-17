<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>日志事件</el-breadcrumb-item>
        <el-breadcrumb-item>日志中心</el-breadcrumb-item>
      </el-breadcrumb>
      <el-tabs v-model="log_type" type="border-card" class="tabs-margin-top">
          <el-tab-pane label="系统日志" name="1">
              <log-table :log_type="1"></log-table>
          </el-tab-pane>
          <el-tab-pane label="采集日志" name="2">
              <log-table :log_type="2"></log-table>
          </el-tab-pane>
          <el-tab-pane label="传输日志" name="3">
              <log-table :log_type="3"></log-table>
          </el-tab-pane>
          <el-tab-pane label="网络日志" name="4">
              <log-table :log_type="4"></log-table>
          </el-tab-pane>
          <el-tab-pane label="权限日志" name="5">
              <log-table :log_type="5"></log-table>
          </el-tab-pane>
      </el-tabs>
  </el-main>
</template>

<script>
import logTable from './components/logTable'
export default {
  data () {
    return {
      log_type: '1'
    }
  },
  components: {
    logTable
  }
}
</script>

<style scoped>

</style>
