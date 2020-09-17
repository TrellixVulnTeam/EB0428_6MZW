<template>
  <el-main class="no-padding">
      <el-form
        inline="true"
        :model="timeForm"
        ref="timeForm"
        :rules="timeRules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item label="选择查询时间:">
          <el-date-picker
            v-model="queryTime"
            size="small"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tableData">

      </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      queryTime: '',
      tableData: []
    };
  },
  props: {
    activeName: {
      type: String,
      required: true,
      default: "1"
    }
  }
};
</script>

<style scoped>
</style>
