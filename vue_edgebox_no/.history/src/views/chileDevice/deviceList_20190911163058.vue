<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
        <el-button type="primary" size="small">新增</el-button>
         <el-input placeholder="请输入内容" v-model="input3" class="pull-right">

         </el-input>
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
