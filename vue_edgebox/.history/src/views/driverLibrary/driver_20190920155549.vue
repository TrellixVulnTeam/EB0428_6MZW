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
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchDrive: '',
    }
  },
}
</script>

<style scoped>

</style>
