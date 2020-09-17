<template>
  <el-container class="container-style">
      <el-header height="50px" class="no-padding">
          <header></header>
      </el-header>
      <el-container>
          <el-aside width="200px">
              <aside></aside>
          </el-aside>
          <el-main>
              <router-view :key="key"></router-view>
          </el-main>
      </el-container>
  </el-container>
</template>

<script>
import HeaderMenu from '../components/HeaderMenu.vue';
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
