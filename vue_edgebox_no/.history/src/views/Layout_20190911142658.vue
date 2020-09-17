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
import Header from '../components/Header.vue';
import Aside from '../components/Aside.vue';
export default {
  data() {
    return {

    }
  },
  components: {
      Header,
      Aside
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
