<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>日志事件</el-breadcrumb-item>
        <el-breadcrumb-item>通知管理</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="row-padding">
          <el-button type="primary" size="small">新增</el-button>
          <el-input size="small" placeholder="请输入内容" v-model="searchEvent" class="search-input pull-right">
           <el-button slot="append" icon="el-icon-search"></el-button>
         </el-input>
      </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchEvent: '',
        tableData: []
    }
  },
}
</script>

<style scoped>

</style>
