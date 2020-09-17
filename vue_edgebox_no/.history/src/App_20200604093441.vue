<template>
  <div id="app" >
    <router-view/>
  </div>
</template>

<style lang="scss">
body{
  overflow: hidden;
}

.el-header{
  z-index: 3000;
}

.el-message{
  z-index: 6000!important
}
</style>

<script>
export default {
  data(){
    return{
    }
  },
  created(){
  },
  mounted(){
  },
  methods:{
  }
}
</script>
