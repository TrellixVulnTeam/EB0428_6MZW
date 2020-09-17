<template>
  <el-container class="container-style">
      <el-header height="50px" class="no-padding">
          <header-menu></header-menu>
      </el-header>
      <el-container>
          <el-aside width="200px">
              <aside-menu></aside-menu>
          </el-aside>
          <el-main>
              <router-view :key="key"></router-view>
          </el-main>
      </el-container>
  </el-container>
</template>

<script>
import HeaderMenu from '../components/HeaderMenu.vue';
import AsideMenu from '../components/AsideMenu.vue';
export default {
  data() {
    return {

    }
  },
  components: {
      HeaderMenu,
      AsideMenu
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
