<template>
  <div >
    <van-row>
      <van-col span="8">
        <van-button type="primary" size="mini">主要</van-button>
      </van-col>
      <van-col span="8">
        <van-button type="info" size="mini">信息</van-button>
      </van-col>
      <van-col span="8">
        <van-button size="mini">默认</van-button>
      </van-col>
    </van-row>
    <van-cell value="12121" title="路由跳转"/>
    <van-cell  />
  </div>
</template>

<script>
export default {
  data () {
    return {}
  }
}
</script>

<style scoped>
>>> .box-color {
  background-color: aqua;
}
</style>
