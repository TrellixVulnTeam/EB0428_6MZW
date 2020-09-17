<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>远程管理及维护</el-breadcrumb-item>
      <el-breadcrumb-item>远程管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-small-padding">
      <el-alert title="配置采集协议用来" type="info" show-icon></el-alert>
    </el-row>

  </el-main>
</template>

<script>
export default {
  data() {
    return {

    }
  },
}
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0; 
}
</style>
