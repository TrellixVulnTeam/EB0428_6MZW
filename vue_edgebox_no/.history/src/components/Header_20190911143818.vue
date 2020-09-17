<template>
  <el-header height="60px" class="header-style">
       <div class="imgBox">
      <!-- <i class="el-icon-user login-icon" @click="loginBoss()"></i> -->
      <el-dropdown>
        <div>
          <!-- <div class="img-back"></div> -->
          <el-button class="pull-right back-btn" type="text" >{{userInfo.account}}</el-button>
        </div>
        <el-dropdown-menu slot="dropdown" class="list-button-tool">
          <el-dropdown-item>
            <el-button type="text" size="small" @click="loginOut">退出</el-button>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </el-header>
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
.header-style {
    padding: 0;
    background-color: #112538;
}
</style>
