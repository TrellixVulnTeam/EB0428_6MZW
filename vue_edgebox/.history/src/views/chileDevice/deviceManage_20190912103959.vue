<template>
  <el-main class="no-padding">
       <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: 'deviceList' }">子设备列表</el-breadcrumb-item>
      <el-breadcrumb-item>采集协议</el-breadcrumb-item>
      <el-breadcrumb-item>特征提取</el-breadcrumb-item>
      <el-breadcrumb-item>数据转发</el-breadcrumb-item>
    </el-breadcrumb>
    
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

</style>
