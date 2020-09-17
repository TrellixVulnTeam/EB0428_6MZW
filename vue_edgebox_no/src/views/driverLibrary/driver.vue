<template>
  <el-main class="no-padding">
      <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>设备驱动库</el-breadcrumb-item>
      <el-breadcrumb-item>驱动库</el-breadcrumb-item>
    </el-breadcrumb>
      <el-row class="row-padding">
          <el-button type="primary" size="small" disabled>新增</el-button>
          <el-input size="small" placeholder="请输入内容" v-model="searchDrive" class="search-input pull-right">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
      </el-row>
      <el-table :data="tableData">
          <el-table-column label="驱动名称" prop="drive_name"></el-table-column>
          <el-table-column label="驱动类型" prop="drive_type">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.drive_type === 'Modbus-RTU'" size="medium">{{ scope.row.drive_type }}</el-tag>
              <el-tag v-else size="medium" type="success">{{ scope.row.drive_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="创建时间" prop="create_time"></el-table-column>
          <el-table-column label="描述" prop="drive_remark"></el-table-column>
          <el-table-column  width="150" label="操作">
              <template>
                  <el-button type="text" size="small" @click="deleteDrive">删除</el-button>
              </template>
              
          </el-table-column>
      </el-table>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        searchDrive: '',
        tableData: [
            {
                drive_name: 'ModbusTcpDemo',
                drive_type: 'ModBus',
                create_time: '2019-05-25 13:52:47',
                drive_remark: 'ModBus采集程式'
            }
        ]
    }
  },
  created() {
    this.$axios.get("apis/drive/list/")
      .then(response => {
        this.tableData = response.data.db;
      })
  },
  methods: {
      // 删除驱动
      deleteDrive() {
          this.$Message.WarningAlert(this, '确定删除选择的驱动吗？', '删除驱动');
      }
  }
}
</script>

<style scoped>

</style>
