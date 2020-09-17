<template>
   <el-menu
     
      class="el-menu-style"
      :unique-opened="true"
      background-color="#112538"
      text-color="#fff"
      active-text-color="#3287B2"
      router
      :collapse="flase">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-printer"></i>
          <span>网关管理</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="gatewayList">网关信息</el-menu-item>
          <el-menu-item index="gatewaySysInfo">系统信息</el-menu-item>
          <el-menu-item index="gatewayServer">网关服务</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-s-tools"></i>
          <span>子设备管理</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="deviceList">设备列表</el-menu-item>
          <el-menu-item index="template">设备模板库</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <!-- <el-menu-item index="deviceList">
          <i class="el-icon-setting"></i>
          <span slot="title">子设备管理</span>  
      </el-menu-item> -->
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
            <span slot="title">事件报警</span>
        </template>
        <el-menu-item-group>
          <!-- <el-menu-item index="logCenter">日志中心</el-menu-item> -->
          <el-menu-item index="eventCenter">
            <!-- <el-badge is-dot class="item"> -->
              <span>事件中心</span>
            <!-- </el-badge> -->

          </el-menu-item>
          <el-menu-item index="notificationManage">通知管理</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="5">
        <template slot="title">
          <i class="el-icon-coin"></i>
          <span slot="title">设备驱动库</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="driver">驱动库</el-menu-item>
          <!-- <el-menu-item index="template">模板库</el-menu-item> -->
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="6">
         <template slot="title">
          <i class="el-icon-set-up"></i>
          <span slot="title">智能产品对接</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="smartDevice">智能设备列表</el-menu-item>
          <el-menu-item index="smartSetting">即插即用设置</el-menu-item>
          <el-menu-item index="smartRemote">智能设备下发</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
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
.el-menu-style:not(.el-menu--collapse) {
  height: 100%;
  width: 199px;
  position: fixed;
  // top: 50px;
  // left: 0;
  // min-height: 625px;
}
.el-icon-printer:before {
  color: beige;
}
.el-icon-s-tools:before {
  color: beige;
}
.el-icon-s-platform:before {
  color: beige;
}
.el-icon-notebook-1:before {
  color: beige;
}
.el-icon-coin:before {
  color: beige;
}
.el-icon-set-up:before{
  color: beige;
}

.el-submenu .el-menu-item{
    min-width: 199px;
  }
</style>
