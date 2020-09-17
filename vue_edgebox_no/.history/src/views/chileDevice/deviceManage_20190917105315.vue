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
    <el-row class="row-padding-top">
      <el-tabs v-model="activeName" type="border-card">
        <el-tab-pane label="采集协议" name="1">
            <acquisition-protocol></acquisition-protocol>
        </el-tab-pane>
        <el-tab-pane label="特征提取" name="2">
          <ffeature-extraction></ffeature-extraction>
        </el-tab-pane>
        <el-tab-pane label="数据转发" name="3">

        </el-tab-pane>
      </el-tabs>
    </el-row>
    <!-- 显示的页面 -->
    
  </el-main>
</template>

<script>
import acquisitionProtocol from './components/acquisitionProtocol.vue';
import featureExtraction from './components/featureExtraction';
export default {
  data() {
    return {
      activeName: "1"
    };
  },
  components: {
      acquisitionProtocol,
      featureExtraction
  }
};
</script>

<style scoped>
.card-style {
  min-width: 400px;
  width: 100%;
}
</style>
