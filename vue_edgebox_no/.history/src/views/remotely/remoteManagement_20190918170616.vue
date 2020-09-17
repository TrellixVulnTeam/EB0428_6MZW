<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>远程管理及维护</el-breadcrumb-item>
      <el-breadcrumb-item>远程管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-small-padding">
      <el-alert title="配置采集协议用来" type="info" show-icon></el-alert>
    </el-row>
    <el-tabs v-model="activeName" type="border-card">
      <el-tab-pane label="Topic" name="1">
        <el-table :data="topicData">
          <el-table-column label="发布类型" prop="type"></el-table-column>
          <el-table-column label="MQTT的Topic" prop="topic"></el-table-column>
          <el-table-column label="状态" prop="description"></el-table-column>
          <el-table-column label="操作" >
            <template>
              <el-button type="text" size="small">使用说明</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="挂载" name="2"></el-tab-pane>
      <el-tab-pane label="网络" name="3"></el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      activeName: '1',
      topicData: [
        {
          type: 'Create',
          topic: '/data/EdgeBox/gateway/create/....',
          description: '创建'
        },
        {
          type: 'Update',
          topic: '/data/EdgeBox/gateway/update/....',
          description: '更新'
        },
        {
          type: 'Delete',
          topic: '/data/EdgeBox/gateway/delete/....',
          description: '删除'
        }
      ]
    }
  },
}
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0; 
}
</style>
