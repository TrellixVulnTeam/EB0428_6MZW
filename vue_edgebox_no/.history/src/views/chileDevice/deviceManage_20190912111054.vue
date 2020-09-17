<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: 'deviceList' }">子设备列表</el-breadcrumb-item>
      <el-breadcrumb-item v-if="activeName === '1'">采集协议</el-breadcrumb-item>
      <el-breadcrumb-item v-else-if="activeName === '2'">特征提取</el-breadcrumb-item>
      <el-breadcrumb-item v-else-if="activeName === '3'">数据转发</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 菜单栏 -->
    <el-row class="row-padding">
      <el-tabs v-model="activeName" type="border-card">
        <el-tab-pane label="采集协议" name="1">采集协议</el-tab-pane>
        <el-tab-pane label="特征提取" name="2">特征提取</el-tab-pane>
        <el-tab-pane label="数据转发" name="3">数据转发</el-tab-pane>
      </el-tabs>
      <acquisition-protocol v-if="activeName === '1'"></acquisition-protocol>
    </el-row>
    
    <!-- 显示的页面 -->
  </el-main>
</template>

<script>
import acquisitionProtocol from './components/acquisitionProtocol.vue';
export default {
  data() {
    return {
      activeName: "1"
    };
  },
  components: {
      acquisitionProtocol
  }
};
</script>

<style scoped>
</style>
