<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">网关管理</el-breadcrumb-item>
      <el-breadcrumb-item>网关信息</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row>
      <el-button type="primary" size="small" icon="el-icon-edit">编辑</el-button>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style scoped>
</style>
