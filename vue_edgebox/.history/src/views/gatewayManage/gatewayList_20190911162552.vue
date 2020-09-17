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
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="ID" prop="id"></el-table-column>
      <el-table-column label="子设备数" prop="childDevices"></el-table-column>
      <el-table-column label="厂商型号" prop="factoryModel"></el-table-column>
      <el-table-column label="厂商名称" prop="factoryName"></el-table-column>
      <el-table-column label="注册时间" prop="registrationTime"></el-table-column>
      <el-table-column label="描述" prop="description"></el-table-column>
      <el-table-column label="位置信息" prop="locationInfo"></el-table-column>
      <el-table-column label="恢复出厂日期" prop="restoreTime"></el-table-column>
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
          registrationTime: '2019-08-31 18:27:02',
          description: 'EdgeBox边缘层网关测试版',
          locationInfo: 'E5-4F',
          restoreTime: '2019-08-31 18:27:02'
        }
      ]
    };
  }
};
</script>

<style scoped>
</style>
