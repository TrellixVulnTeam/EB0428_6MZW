<template>
  <el-container>
      <el-header>

      </el-header>
      <el-container>
          <el-aside width="200">

          </el-aside>
          <el-main>
              <router-view :key="key"></router-view>
          </el-main>
      </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {

    }
  },
  computed: {
      key () {
        return this.$route.fullPath
      }
    }
}
</script>

<style scoped>

</style>
