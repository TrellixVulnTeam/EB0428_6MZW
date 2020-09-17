<template>
  <el-main class="no-padding">
      <el-tabs v-model="activeName" type="border-card">
          <el-tab-pane label="系统日志" name="1">
              <log-table :activeName="activeName"></log-table>
          </el-tab-pane>
          <el-tab-pane label="采集日志" name="2">
              <log-table :activeName="activeName"></log-table>
          </el-tab-pane>
          <el-tab-pane label="传输日志" name="3">
              <log-table :activeName="activeName"></log-table>
          </el-tab-pane>
          <el-tab-pane label="网络日志" name="4">
              <log-table :activeName="activeName"></log-table>
          </el-tab-pane>
          <el-tab-pane label="权限日志" name="5">
              <log-table :activeName="activeName"></log-table>
          </el-tab-pane>
      </el-tabs>
  </el-main>
</template>

<script>
import logTable from './components/logTable';
export default {
  data() {
    return {
        activeName: '1'
    }
  },
  components: {
      logTable
  }
}
</script>

<style scoped>

</style>
