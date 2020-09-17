<template>
  <el-main class="no-padding">
      <el-row class="row-padding">
          <el-input placeholder="请输入内容" v-model="searchEvent" class="input-with-select">
           <el-button slot="append" icon="el-icon-search"></el-button>
         </el-input>
      </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchEvent: ''
    }
  },
}
</script>

<style scoped>

</style>
