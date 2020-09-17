<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
        <el-button type="primary" size="small">新增</el-button>
        <el-button type="primary" size="small" disabled>批量删除</el-button>
        <el-button type="primary" size="small" disabled>批量禁用</el-button>
        <el-button type="primary" size="small" disabled>批量启用</el-button>
         <el-input placeholder="请输入内容" size="small" v-model="searchDevice" class="pull-right search-input">
             <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
         </el-input>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchDevice: '', // 搜索设备名称
    };
  }
};
</script>

<style scoped>
</style>
