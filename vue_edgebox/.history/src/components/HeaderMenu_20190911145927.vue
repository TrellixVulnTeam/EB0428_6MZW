<template>
  <el-header height="50px" class="header-style">
    <div class="imgBox">
      <el-dropdown>
        <div>
          <el-button class="pull-right back-btn" type="text">
            <i class="fa fa-user user-icon"></i>&nbsp;
            admin
          </el-button>
        </div>
        <el-dropdown-menu slot="dropdown" class="list-button-tool">
          <el-dropdown-item>
            <el-button type="text" size="small">退出</el-button>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style scoped>
.header-style {
  padding: 0;
  width: 100%;
  min-width: 1200px;
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

.user-icon {
  color: #fff;
}
</style>
