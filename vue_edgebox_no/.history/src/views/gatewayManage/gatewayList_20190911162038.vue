<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">网关管理</el-breadcrumb-item>
      <el-breadcrumb-item>网关信息</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-button size="small" icon="el-icon-edit">编辑</el-button>
    </el-row>
    <el-table :data="tableData" border>
      <el-table-column label="名称"></el-table-column>
      <el-table-column label="ID"></el-table-column>
      <el-table-column label="子设备数"></el-table-column>
      <el-table-column label="厂商型号"></el-table-column>
      <el-table-column label="厂商名称"></el-table-column>
      <el-table-column label="注册时间"></el-table-column>
      <el-table-column label="描述"></el-table-column>
      <el-table-column label="位置信息"></el-table-column>
      <el-table-column label="恢复出厂日期"></el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      tableData: [
        {
          name: 'EdgeBox003',
          id: '6553791093879608705',
          childDevices: '10',
          factoryModel: 'IoT',
          factoryName: 'IoT',
        }
      ]
    };
  }
};
</script>

<style scoped>
</style>
