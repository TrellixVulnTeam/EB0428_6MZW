<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>设备驱动库</el-breadcrumb-item>
      <el-breadcrumb-item>模板库</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-alert title="设备模板库是网关可以为用户保存经常使用的设备通用配置" type="info" show-icon></el-alert>
    </el-row>
    <el-table :data="tableData"  ref="refTable" @row-click="clickTable">
        <el-table-column label="模板名称" prop="name"></el-table-column>
        <el-table-column label="协议名称" prop="protocol">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.protocol === 'Modbus-RTU'" size="medium">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else size="medium" type="success">{{ scope.row.protocol }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="createTime"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="100">
            <template>
                <el-button type="text" size="small">删除</el-button>
            </template>
        </el-table-column>
         <el-table-column type="expand">
            <template v-slot="scope">
               <el-row  v-for="(key , i) in scope.row.info " :key ="Number(i)">
                  <el-col v-for="(v, j) in key " :key ="Number(j)" :span="6" >
                    <json-viewer
                      :value="v"
                      :expand-depth="1"
                      copyable
                      boxed
                      sort
                    ></json-viewer>
                  </el-col>
                  <br>
               </el-row>
            </template>
        </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  data () {
    return {
      entdatas: [],
      entexpands: [],
      tableData: []
    }
  },
  created () {
    this.$axios.get('apis/device/template') // 设备协议清单
      .then(response => {
        this.tableData = response.data.db
      })
  },
  methods: {
    clickTable (row, index, e) {
      this.$refs.refTable.toggleRowExpansion(row)
    }

  }
}

</script>

<style scoped>
.el-col-6 {
  padding: 5px;
}
</style>
