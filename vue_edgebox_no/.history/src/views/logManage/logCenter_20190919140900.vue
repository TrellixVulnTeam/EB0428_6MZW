<template>
  <el-main class="no-padding">
      <el-tabs v-model="activeName" type="border-card">
          <el-tab-pane label="采集协议" name="1"></el-tab-pane>
      </el-tabs>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        activeName: '1'
    }
  },
}
</script>

<style scoped>

</style>
