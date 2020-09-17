<template>
  <div id="app" >
    <router-view/>
  </div>
</template>

// <style lang="scss">
// body{
//   overflow: hidden;
// }

// .el-header{
//   z-index: 3000;
// }

// .el-message{
//   z-index: 6000!important
// }
// </style>

<script>
export default {
  data(){
    return{
      isFullscreen: false
    }
  },
  created(){
    // document.title = "登录"
    this.$secre.changeSecret(this.$secre.secretkey("123!@#abc阿萨德"))
  },
  mounted(){
    this.$screenfull.on('change', () => {
        // console.log('Am I fullscreen?', this.$screenfull.isFullscreen ? 'Yes' : 'No');
        // if(this.$screenfull.isFullscreen == false) this.getInfo()
    });
    this.$screenfull.on('error', event => {
        // console.error('Failed to enable fullscreen', event);
    });
    // screenfull.off('change', callback);
  },
  methods:{
    getInfo(){
      
      // this.$screenfull.toggle()
      this.$screenfull.request()
      // if (!this.$screenfull.enabled) { // 如果不允许进入全屏，发出不允许提示
      //   this.$message({
      //     message: '不支持全屏',
      //     type: 'warning'
      //   })
      //   return false
      // }
      // this.$screenfull.toggle()
      // this.$message({
      //   message: '全屏啦',
      //   type: 'success'
      // })
    }
  }
}
</script>
