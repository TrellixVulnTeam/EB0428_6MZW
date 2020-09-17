<template>
   <el-menu
      default-active="deviceList"
      class="el-menu-style"
      :unique-opened="true"
      background-color="#112538"
      text-color="#fff"
      active-text-color="#3287B2"
      router>
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-printer"></i>
          <span>网关管理</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="gatewayList">网关信息</el-menu-item>
          <el-menu-item index="1-2">系统信息</el-menu-item>
          <el-menu-item index="1-2">网关服务</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-menu-item index="deviceList">
          <i class="el-icon-setting"></i>
          <span slot="title">子设备管理</span>  
      </el-menu-item>
      <el-submenu index="3">
        <template slot="title">
          <i class="el-icon-s-platform"></i>
          <span slot="title">远程管理及维护</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="configuration">配置下发</el-menu-item>
          <el-menu-item index="remoteManagement">远程管理</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="4">
        <template  slot="title">
          <i class="el-icon-notebook-1"></i>
          <span slot="title">日志事件</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="logCenter">日志中心</el-menu-item>
          <el-menu-item index="4-2">事件中心</el-menu-item>
          <el-menu-item index="4-3">通知管理</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="5">
        <template slot="title">
          <i class="el-icon-coin"></i>
          <span slot="title">设备驱动库</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="5-1">驱动库</el-menu-item>
          <el-menu-item index="5-2">模板库</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-menu-item index="#">
        <i class="el-icon-set-up"></i>
        <span slot="title">M5对接模块</span>
      </el-menu-item>
    </el-menu>
</template>

<script>
export default {
  data() {
    return {

    }
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
.el-menu-style {
  height: 100%;
  width: 199px;
  // min-height: 625px;
}

.el-submenu .el-menu-item{
    min-width: 199px;
  }
</style>
