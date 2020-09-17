<template>
  <el-header height="50px" class="header-style">
    <div class="imgBox">
    <div class="demo-image__preview">
      <el-image 
        :src="url" 
        :preview-src-list="srcList">
        <div slot="error" class="image-slot">
          <i class="el-icon-picture-outline"></i>
        </div>
      </el-image>
    </div>
    </div>
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
     return {
        url: require('../assets/helpimg/bj.png'),
        srcList: [
          require('../assets/helpimg/1.png'),
          require('../assets/helpimg/2.png'),
        ]
      }
  },
  methods: {
    getSrcList(index){
      return this.srcList.slice(index).concat(this.srcList.slice(0,index))
    }
  }
};
</script>

<style scoped>
.header-style {
  padding: 0;
  width: 100%;
  min-width: 1200px;
  background-color: #112538;
  position: fixed;
  z-index: 2000;
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
