<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>设备驱动库</el-breadcrumb-item>
      <el-breadcrumb-item>模板库</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-alert title="提示：每个设备最多可配置四条转发路径" type="info" show-icon></el-alert>
    </el-row>
    <el-table :data="tableData">

    </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        tableData: [
            {
                name: '',
                protocolL: '',
            }
        ]
    };
  }
};
</script>

<style scoped>
</style>
