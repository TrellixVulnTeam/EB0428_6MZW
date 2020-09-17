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
        <el-table-column label="模板名称" prop="name"></el-table-column>
        <el-table-column label="协议名称" prop="protocol"></el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        tableData: [
            {
                name: 'HC31A电表',
                protocol: 'ModBus',
                createTime: '2019-05-25 13:52:47',
                description: 'HC31A电表配置模板'
            },
            {
                name: 'HC31A电表',
                protocol: 'ModBus',
                createTime: '2019-05-25 13:52:47',
                description: 'HC31A电表配置模板'
            },
            {
                name: 'HC31A电表',
                protocol: 'ModBus',
                createTime: '2019-05-25 13:52:47',
                description: 'HC31A电表配置模板'
            }
        ]
    };
  }
};
</script>

<style scoped>
</style>
