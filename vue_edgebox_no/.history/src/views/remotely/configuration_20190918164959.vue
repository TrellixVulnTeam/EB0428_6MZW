<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>远程管理及维护</el-breadcrumb-item>
      <el-breadcrumb-item>配置下发</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-small-padding">
      <el-alert title="该功能实现远程对网关的配置下发！" type="info" show-icon></el-alert>
    </el-row>
    <el-table :data="tableData">
      <el-table-column label="下发类型" prop="type"></el-table-column>
      <el-table-column label="MQTT的Topic">
        <template v-slot="scope">
          <span>{{scope.row.topic}}</span>&nbsp;
          <el-button type="text" class="el-icon-document tag-read" @click="paste(scope.$index)"></el-button>
        </template>
      </el-table-column>
      <el-table-column label="描述" prop="description"></el-table-column>
      <el-table-column label="操作">
        <template>
          <el-button type="text" size="small">使用说明</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
import Clipboard from 'clipboard';
import { SuccessMessage, ErrorMessage } from '../../message/message.js';
export default {
  data() {
    return {
      tableData: [
        {
          type: 'Create',
          topic: '/data/EdgeBox/gateway/create/....',
          description: '创建新设备'
        },
        {
          type: 'Update',
          topic: '/data/EdgeBox/gateway/update/....',
          description: '修改设备'
        },
        {
          type: 'Delete',
          topic: '/data/EdgeBox/gateway/delete/....',
          description: '删除设备'
        }
      ]
    };
  },
  methods: {
    // 复制tpoic
    paste(index) {
      let topic = this.tableData[index].topic;
      let clipboard = new Clipboard('.tag-read', {
            text: function() {
                return topic;
            }
      });
       // 复制成功
       clipboard.on('success', e => {
          this.$Message.SuccessMessage(this, '复制成功');
          // 释放内存
          clipboard.destroy()
        })
        // 不支持复制
        clipboard.on('error', e => {
          
          
          // 释放内存
          clipboard.destroy()
        });
    },
  }
};
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0; 
}

.tag-read {

}
</style>
