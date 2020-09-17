<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>日志事件</el-breadcrumb-item>
        <el-breadcrumb-item>事件中心</el-breadcrumb-item>
      </el-breadcrumb>
      <event-table></event-table>
  </el-main>
</template>

<script>
import eventTable from './components/eventTable'
export default {
  data () {
    return {
    }
  },
  components: {
    eventTable
  }
}
</script>

<style scoped>

</style>
