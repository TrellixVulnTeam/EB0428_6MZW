<template>
  <el-header height="3.1em" class="header-style">
  <!-- <el-header height="60px" class="header-style"> -->
    <div class="imgBox" style="height: 100%;line-height: 200%;width: 6em;margin: 0 auto;">
    <!-- <div class="imgBox" style="position:relative;height: 100%;width: 120px;margin: 0 auto;"> -->
      <el-dropdown @command="handleCommand" trigger="click">
        <div>
          <el-button class="pull-right back-btn" type="text" style="line-height:200%">
          <!-- <el-button class="pull-right back-btn" type="text" style="line-height:240%"> -->
            <i class="fa fa-user user-icon"></i>&nbsp;
            {{userName}}
          </el-button>
        </div>
        <el-dropdown-menu slot="dropdown" class="list-button-tool">
          <el-dropdown-item command="userCenter">
            <el-button type="text" size="small">用户中心</el-button>
          </el-dropdown-item>
          <el-dropdown-item command="Exit">
            <el-button type="text" size="small">退出</el-button>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script>
export default {
  data () {
    return {
      userName:''
    }
  },
  created(){
    if(localStorage.getItem("tokenLogin")){
      this.userName = JSON.parse(this.$secre.changeSecret(localStorage.getItem("tokenLogin")))['name'];
    }
  },
  methods:{
      handleCommand(command) {
        var _this = this
        if(command == "Exit"){
          this.$axios.get('user/login/change')
              .then(response => {
                  localStorage.removeItem("tokenLogin")
                  _this.$router.push({
                    name: "Login"
                  });
                  this.$Message.SuccessMessage(this, "成功登出")        
              })
        }
        if(command == "userCenter"){
          $(".el-user-center").click()
        }
      },
  }
}
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
/* .el-dropdown{
  position: absolute;
  height: 100%;
} */
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
