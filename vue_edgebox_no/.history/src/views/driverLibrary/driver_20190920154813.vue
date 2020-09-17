<template>
  <el-main class="no-padding">
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

    }
  },
}
</script>

<style scoped>

</style>
