<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-button type="primary" size="small">新增</el-button>
      <el-button size="small" disabled>批量删除</el-button>
      <el-button size="small" disabled>批量禁用</el-button>
      <el-button size="small" disabled>批量启用</el-button>
      <el-input
        placeholder="请输入内容"
        size="small"
        v-model="searchDevice"
        class="pull-right search-input"
      >
        <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
    <el-table :data="tableData" stripe   ref="multipleTable"
    tooltip-effect="dark"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="类型" prop="type"></el-table-column>
      <el-table-column label="位置" prop="position"></el-table-column>
      <el-table-column label="型号" prop="model"></el-table-column>
      <el-table-column label="描述" prop="description"></el-table-column>
      <el-table-column label="最近上线时间" prop="time"></el-table-column>
      <el-table-column label="启用/禁用">
        <template v-slot="scope">
          <el-switch v-model="scope.row.operating" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="状态" prop="status"></el-table-column>
      <el-table-column label="操作">
        <template>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="收货地址" :visible.sync="dialogFormVisible">
  <el-form :model="form">
    <el-form-item label="活动名称" :label-width="formLabelWidth">
      <el-input v-model="form.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="活动区域" :label-width="formLabelWidth">
      <el-select v-model="form.region" placeholder="请选择活动区域">
        <el-option label="区域一" value="shanghai"></el-option>
        <el-option label="区域二" value="beijing"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
    </el-dialog>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      searchDevice: "", // 搜索设备名称
      tableData: [
        {
          name: "342432",
          type: "压铸设备类",
          position: "E5-4F",
          model: "isokets",
          description: "智能电表",
          time: "2019年8月17日 14:12",
          operating: true,
          status: "离线"
        },
        {
          name: "342432",
          type: "压铸设备类",
          position: "E5-4F",
          model: "isokets",
          description: "智能电表",
          time: "2019年8月17日 14:12",
          operating: false,
          status: "离线"
        },
        {
          name: "342432",
          type: "压铸设备类",
          position: "E5-4F",
          model: "isokets",
          description: "智能电表",
          time: "2019年8月17日 14:12",
          operating: false,
          status: "离线"
        }
      ]
    };
  },
  methods: {
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      }
    }
};
</script>

<style scoped>
</style>
