<template>
  <el-main class="no-padding">
      <el-row class="row-padding">
          <el-form>
              <el-form-item></el-form-item>
              <el-form-item></el-form-item>
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
