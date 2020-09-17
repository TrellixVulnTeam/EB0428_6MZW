<template>
  <el-main class="no-padding">
      <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>设备驱动库</el-breadcrumb-item>
      <el-breadcrumb-item>驱动库</el-breadcrumb-item>
    </el-breadcrumb>
      <el-row class="row-padding">
          <el-button type="primary" size="small">新增</el-button>
          <el-input size="small" placeholder="请输入内容" v-model="searchDrive" class="search-input pull-right">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
      </el-row>
      <el-table :data="tableData">
          <el-table-column label="驱动名称" prop="name"></el-table-column>
          <el-table-column label="驱动类型" prop="type"></el-table-column>
          <el-table-column label="创建时间" prop="createTime"></el-table-column>
          <el-table-column label="描述" prop="description"></el-table-column>
          <el-table-column label="操作">
              <el-button type="text" size="small">删除</el-button>
          </el-table-column>
      </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchDrive: '',
        tableData: [
            {
                name: 'ModBus',
                type: 'ModBus',
                createTime: '2019-05-25 13:52:47',
                description: ''
            }
        ]
    }
  },
}
</script>

<style scoped>

</style>
