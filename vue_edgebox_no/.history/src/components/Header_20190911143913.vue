<template>
  <el-header height="60px" class="header-style">
       <div class="imgBox">
      <!-- <i class="el-icon-user login-icon" @click="loginBoss()"></i> -->
      <el-dropdown>
        <div>
          <!-- <div class="img-back"></div> -->
          <el-button class="pull-right back-btn" type="text" >admin</el-button>
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

.imgBox {
  /* // border-radius: 50%;
  // width: 30px;
  // height: 30px; */
  margin-top: 5px;
  /* // background-color: white; */
  float: right;
  margin-right: 40px;
}
.img-back {
  border-radius: 50%;
  width: 30px;
  height: 30px;
  margin-top: 5px;
  background-color: #fff;
  display: inline-block;
  margin-right: 10px;
  /* // float: left; */
}

.back-btn {
  color: #fff;
}

.login-icon {
  color: #fff;
  font-size: 25px;
  line-height: 40px;
  cursor: pointer;
}
</style>
