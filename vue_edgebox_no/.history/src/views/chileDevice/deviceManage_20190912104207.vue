<template>
  <el-main class="no-padding">
       <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: 'deviceList' }">子设备列表</el-breadcrumb-item>
      <el-breadcrumb-item>采集协议</el-breadcrumb-item>
      <el-breadcrumb-item>特征提取</el-breadcrumb-item>
      <el-breadcrumb-item>数据转发</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 菜单栏 -->
    <el-tabs v-model="activeName" type="border-card">
      <el-tab-pane label="用户管理">用户管理</el-tab-pane>
      <el-tab-pane label="配置管理">配置管理</el-tab-pane>
      <el-tab-pane label="角色管理">角色管理</el-tab-pane>
      <el-tab-pane label="定时任务补偿">定时任务补偿</el-tab-pane>
    </el-tabs>
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
