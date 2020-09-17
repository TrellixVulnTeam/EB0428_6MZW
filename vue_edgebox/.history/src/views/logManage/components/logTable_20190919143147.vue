<template>
  <el-main class="no-padding">
      <el-row class="row-padding">
          <el-form inline="true" :model="timeForm" ref="timeForm" :rules="timeRules" label-width="100px" label-position="left">
              <el-form-item label="起始时间:">

              </el-form-item>
              <el-form-item label="终止时间:">

              </el-form-item>
              <el-form-item>

              </el-form-item>
          </el-form>
      </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {

    }
  },
  props: {
      activeName: {
          type: String,
          required: true,
          default: '1'
      }
  }
}
</script>

<style scoped>

</style>
