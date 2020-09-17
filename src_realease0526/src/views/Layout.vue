<template>
  <el-container class="container-style layout">
    <el-header height="3.1em" class="no-padding">
    <!-- <el-header height="60px" class="no-padding"> -->
      <header-menu></header-menu>
    </el-header>
    <el-container>
      <el-aside width="12em" style="overflow:hidden">
      <!-- <el-aside width="220px" style="overflow:hidden"> -->
        <aside-menu></aside-menu>
      </el-aside>
      <el-main class="ul">
        <router-view :key="key"></router-view>
        </el-main>
    </el-container>
  </el-container>
</template>
<style>
  .layout .el-aside{
    position: relative;
  }
  .layout .el-aside .ul{
    position: absolute;
  }
</style>
<script>
import HeaderMenu from '../components/HeaderMenu.vue'
import AsideMenu from '../components/AsideMenu.vue'
// import login from '../components/login.vue'
export default {
  data () {
    return {
        // 超时定时器
        overTimer: null,
        // 是否超时
        isOvertime: false,
    }
  },
  created(){
  },
  mounted(){
    if(localStorage.getItem("tokenLogin")){
      if(JSON.parse(this.$secre.changeSecret(localStorage.getItem("tokenLogin")))["isLogin"] == false){
        var that = this
        //设置超时退出
        var lastTime = new Date().getTime();
        var currentTime = new Date().getTime();
        var timeOut = 30 * 60 * 1000; //设置超时时间： 30分
        // var timeOut = 1 * 60 * 100; //设置超时时间： 10分
        // var timeOut = 10 * 10 * 100; //设置超时时间： 10秒

        $(function(){
            /* 鼠标移动事件 */
            $(document).mouseover(function(){
                lastTime = new Date().getTime(); //更新操作时间
            });
        });

        function testTime(){
            currentTime = new Date().getTime(); //更新当前时间
            if(!localStorage.getItem("tokenLogin")){
              lastTime = new Date().getTime();
            }
            if(currentTime - lastTime > timeOut){ //判断是否超时
                that.$Message.ErrorMessage(that, '长时间未操作，请重新登录');
                localStorage.removeItem("tokenLogin")
                // clearInterval(that.overTimer)
                if(!localStorage.getItem("ReLogin")){
                  localStorage.setItem("ReLogin",that.$secre.secretkey((that.$route.path).replace("/" , "")))
                }
                
                that.$router.push({
                  path: "SmallLogin"
                })
                // window.location.reload()
            }
        }

        /* 定时器  间隔1秒检测是否长时间未操作页面  */
        this.overTimer = window.setInterval(testTime, 1000);
      }
    }
  },
  destroyed () {
      // 销毁定时器
      // clearTimeout(this.overTimer)
      clearInterval(this.overTimer)
  },
  methods:{
    abc(){
      this.$router.push({path:"/"})
      if(this.$parent.isLogin == true){
        console.log("已登录")
      }else{
        console.log("未登录")
      }
    },
  },
  components: {
    HeaderMenu,
    AsideMenu,
  },
  // props:{
  //     isLogin:Boolean
  // },
  computed: {
    key () {
      return this.$route.fullPath
    }
  },
  //接收子组件的传值，更新父组件的值
  addFolderProp:function(data){
    this.addFolderName = data
  }
}
</script>

<style scoped>

</style>
