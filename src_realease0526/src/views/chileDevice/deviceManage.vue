<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: 'deviceList' }">{{title}}</el-breadcrumb-item>
      <el-breadcrumb-item v-if="activeName === '0'">采集协议 ({{subdevice_name}})</el-breadcrumb-item>
      <el-breadcrumb-item v-else-if="activeName === '1'">特征提取 ({{subdevice_name}})</el-breadcrumb-item>
      <el-breadcrumb-item v-else-if="activeName === '2'">数据转发 ({{subdevice_name}})</el-breadcrumb-item>
      <el-steps  style = "padding-left: 200px ; padding-right: 0px" :space="250" :active="Number(activeName)" finish-status="success" >
        <el-step v-if="title !== '智能设备列表'"  title="Step1: 配置设备采集协议"></el-step>
        <el-step v-else  :title="'Step1: 通道<'+pip_index+'>连接成功'"></el-step>
        <el-step  title="Step2: 设备属性的特征提取"></el-step>
        <el-step  title="Step3: 设备数据转发配置"></el-step>
      </el-steps>
    </el-breadcrumb>
    <!-- 菜单栏 -->
    <el-row class="row-padding-top">
      <el-tabs v-model="activeName" type="border-card"  >
        <el-tab-pane v-if="title !== '智能设备列表'" label="采集协议" :disabled="enable" name= '0' style="overflow-y:auto;overflow-x:hidden;">
            <acquisition-protocol v-if="activeName === '0'"  ></acquisition-protocol>
        </el-tab-pane>
        <el-tab-pane  label="特征提取" name= '1' style="overflow-y:auto;overflow-x:hidden;">
          <feature-extraction v-if="activeName === '1'" ></feature-extraction>
        </el-tab-pane>
        <el-tab-pane label="数据转发" name= '2' style="overflow-y:auto;overflow-x:hidden;">
          <data-forwarding v-if="activeName ==='2'" ></data-forwarding>
        </el-tab-pane>

      </el-tabs>
    </el-row>
    <!-- 显示的页面 -->

  </el-main>
</template>

<script>
import acquisitionProtocol from './components/acquisitionProtocol.vue'
import featureExtraction from './components/featureExtraction.vue'
import dataForwarding from './components/dataForwarding.vue'
import { parse } from 'url'
export default {
  data () {
    return {
      title: '子设备列表',
      enable: false,
      activeName: '0',
      subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
      pip_index: JSON.parse(sessionStorage.getItem('pip_index'))
      // subdevice_name: this.$route.query.subdevice,
    }
  },
  created () {
    this.check()
  },
  components: {
    acquisitionProtocol,
    featureExtraction,
    dataForwarding
  },
  methods: {
    check () {
      var index = JSON.parse(sessionStorage.getItem('pip_index'))
      if (index === '01' || index === '02' || index === '03' || index === '04') {
        this.activeName = '2'
        this.enable = true
        this.title = '智能设备列表'
      }
    }

  }
}
</script>

<style >
.el-step__icon {
    width: 20px;
    height: 21px;
    font-size: 10px;
}
.row-padding-top {
  padding-top: 10px
}
.el-step__title {
    font-size: 10px;
    line-height: 20px;
}
</style>
