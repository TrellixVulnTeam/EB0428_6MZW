<template>
  <el-main class="no-padding">
      <el-tabs v-model="activeName" type="border-card">
          <el-tab-pane label="系统日志" name="1">

          </el-tab-pane>
          <el-tab-pane label="采集日志" name="2">

          </el-tab-pane>
          <el-tab-pane label="传输日志" name="3">

          </el-tab-pane>
          <el-tab-pane label="网络日志" name="4">

          </el-tab-pane>
          <el-tab-pane label="权限日志" name="5">
              
          </el-tab-pane>
      </el-tabs>
      <el-table :data="tableData">
          
      </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        activeName: '1'
    }
  },
}
</script>

<style scoped>

</style>
