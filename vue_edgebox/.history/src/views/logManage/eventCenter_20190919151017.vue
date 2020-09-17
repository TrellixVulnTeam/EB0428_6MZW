<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>日志事件</el-breadcrumb-item>
        <el-breadcrumb-item>日志中心</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="row-padding">
          <el-input size="small" placeholder="请输入内容" v-model="searchEvent" class="search-input pull-right">
           <el-button slot="append" icon="el-icon-search"></el-button>
         </el-input>
      </el-row>
      <el-table :data="tableData">
          <el-table-column label="序号" prop="index"></el-table-column>
          <el-table-column label="事件类型" prop="eventType"></el-table-column>
          <el-table-column label="用户名" prop="userName"></el-table-column>
          <el-table-column label="记录时间" prop="recordingTime"></el-table-column>
          <el-table-column label="事件详情" prop="eventInfo"></el-table-column>
      </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchEvent: '',
        tableData: [
            {
                index: 1,
                eventType: 'information',
                userName: 'F1334747',
                recordingTime: '2019/05/02 02:22',
                eventInfo: 'dirtimealsdidfdfcdtime'
            },
            {
                index: 2,
                eventType: 'information',
                userName: 'F1334747',
                recordingTime: '2019/05/02 02:22',
                eventInfo: 'dirtimealsdidfdfcdtime'
            },
            {
                index: 3,
                eventType: 'information',
                userName: 'F1334747',
                recordingTime: '2019/05/02 02:22',
                eventInfo: 'dirtimealsdidfdfcdtime'
            }
        ]
    }
  },
}
</script>

<style scoped>

</style>
