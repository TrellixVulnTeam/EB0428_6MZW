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
      <el-table :data="tableData">
          <el-table-column label="责任人" prop="responsible"></el-table-column>
          <el-table-column label="位置" prop="position"></el-table-column>
          <el-table-column label="已通知消息数" prop="mesNumber"></el-table-column>
          <el-table-column label="最近通知时间" prop="time"></el-table-column>
          <el-table-column label="通知状态">
              
          </el-table-column>
          <el-table-column label="操作">
              <el-button type="text" size="mini">删除</el-button>
              <el-button type="text" size="mini">详情</el-button>
          </el-table-column>
      </el-table>
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
