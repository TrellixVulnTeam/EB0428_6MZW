<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 操作 -->
    <el-row class="row-padding">
      <el-button type="primary" size="small" @click="dialogFormVisible = true">新增</el-button>
      <el-button size="small" :disabled="deleteBtn">批量删除</el-button>
      <el-button size="small" :disabled="unableBtn">批量禁用</el-button>
      <el-button size="small" :disabled="enableBtn">批量启用</el-button>
      <el-input
        placeholder="请输入内容"
        size="small"
        v-model="searchDevice"
        class="pull-right search-input"
      >
        <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
    <!-- 子设备列表 -->
    <el-table
      :data="tableData"
      stripe
      ref="multipleTable"
      tooltip-effect="dark"
      :row-class-name="tableRowIndexArray"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="类型" prop="type"></el-table-column>
      <el-table-column label="位置" prop="position"></el-table-column>
      <el-table-column label="型号" prop="model"></el-table-column>
      <el-table-column label="描述" prop="description"></el-table-column>
      <el-table-column label="最近上线时间" prop="time"></el-table-column>
      <el-table-column label="启用/禁用">
        <template v-slot="scope">
          <el-switch v-model="scope.row.operating" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="状态" prop="status"></el-table-column>
      <el-table-column label="操作">
        <template>
          <el-button type="text" size="small" @click="dialogFormVisible = true">修改</el-button>
          <el-button type="text" size="small" @click="deleteRow">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 新增设备弹出框 -->
    <el-dialog title="添加子设备" :visible.sync="dialogFormVisible" custom-class="chile-device-box">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="设备名称:" prop="name">
          <el-input type="text" size="small" v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="所属类别:" prop="typeSelect">
          <el-select size="small" style="width: 100%" v-model="form.typeSelect" placeholder="请选择所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备位置:" prop="position">
          <el-input type="text" size="small" v-model="form.position"></el-input>
        </el-form-item>
        <el-form-item label="设备型号:" prop="model">
          <el-input type="text" size="small" v-model="form.model"></el-input>
        </el-form-item>
        <el-form-item label="描述:" >
          <el-input type="textarea" rows="3" v-model="form.description"></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- 修改设备信息弹出框 -->
    <el-dialog title="修改子设备信息" :visible.sync="modifyDialog" custom-class="chile-device-box">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="设备名称:" prop="name">
          <el-input type="text" size="small" v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="所属类别:" prop="typeSelect">
          <el-select size="small" style="width: 100%" v-model="form.typeSelect" placeholder="请选择所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.index">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备位置:" prop="position">
          <el-input type="text" size="small" v-model="form.position"></el-input>
        </el-form-item>
        <el-form-item label="设备型号:" prop="model">
          <el-input type="text" size="small" v-model="form.model"></el-input>
        </el-form-item>
        <el-form-item label="描述:" >
          <el-input type="textarea" rows="3" v-model="form.description"></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
  </el-main>
</template>

<script>
import { checkNull } from '../../until/checkRules'
export default {
  data() {
    return {
      searchDevice: "", // 搜索设备名称
      tableData: [  // 设备列表数据
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
      ],
      dialogFormVisible: false, // 弹出框控制
      multipleSelection: [],
      form: { // 表单元素
          name: '',
          typeSelect: '',
          position: '',
          model: '',
          description: ''
      },
      typeList: [  // 设备类型列表
          {
              index: 0,
              value: '生产设备类'
          },
          {
              index: 1,
              value: '压铸设备类'
          },
          {
              index: 2,
              value: '环境设备类'
          },
          {
              index: 3,
              value: '机床设备类'
          },
          {
              index: 4,
              value: '仪表设备类'
          },
          {
              index: 5,
              value: '注塑成型设备类'
          },
          {
              index: 6,
              value: '包装设备类'
          },
          {
              index: 7,
              value: '工控设备类'
          },
          {
              index: 8,
              value: '传感器设备类'
          },
          {
              index: 9,
              value: 'SMT设备类'
          },
          {
              index: 10,
              value: '冲压设备类'
          },
          {
              index: 11,
              value: '表面处理设备类'
          },
          {
              index: 12,
              value: '运输设备类'
          },
          {
              index: 13,
              value: '其他'
          }
      ],
      rules: { // 表单验证
          name: [
              {
                required: true, validator: checkNull, trigger: 'change'
              }
          ],
          typeSelect: [
              {
                required: true, validator: checkNull, trigger: 'change'
              }
          ],
          position: [
              {
                required: true, validator: checkNull, trigger: 'change'
              }
          ],
          model: [
              {
                required: true, validator: checkNull, trigger: 'change'
              }
          ]
      },
      deleteBtn: true, // 批量删除按钮状态
      enableBtn: true, // 批量启用按钮状态
      unableBtn: true, // 批量禁用按钮状态
      enableRows: [], // 批量启用的数组数据
      unableRows: [], // 批量禁用的数组数据
      modifyDialog: false, // 修改子设备信息弹出框
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
    tableRowIndexArray(row) {
      //设置row对象的index
      row.row.index = row.rowIndex;
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
      console.log(val);
      // 判断批量删除按钮的状态
      this.deleteBtn = this.multipleSelection.length <= 0 ? true : false;
      this.selectRowsData();
    },
    // 判断是否批量启用或禁用
    selectRowsData() {
      let selectRows = this.multipleSelection;
      let enableRows = []; // 启用状态可操作的数据数组
      let enableBtn = true;
      let unableRows = []; // 禁用状态可操作的数据数组
      let unableBtn = true;
      // 筛选数据判断批量启用按钮的状态
      for (let i in selectRows) {
        if (selectRows[i].operating == true) {
          enableBtn = true;
          break;
        } else {
          enableRows.push(selectRows[i]);
          enableBtn = false;
        }
      }
      // 筛选数据判断批量禁用按钮的状态
      for (let i in selectRows) {
        if (selectRows[i].operating == false) {
          unableBtn = true;
          break;
        } else {
          unableRows.push(selectRows[i]);
          unableBtn = false;
        }
      }
      // 批量启用
      this.enableBtn = enableBtn;
      this.enableRows = enableRows;
      // 批量禁用
      this.unableBtn = unableBtn;
      this.unableRows = unableRows;
    },
    // 启用或者禁用
    chooseStatus(row) {
      if (row.operating === true) {
        this.$Message.SuccessMessage(this, '启用成功');
      } else {
        this.$Message.SuccessMessage(this, '禁用成功');
      }
    },
    // 删除数据
    deleteRow() {
      this.$Message.WarningAlert(this,'您确定要删除这条数据吗？','删除');
    },
    // 提交表单
    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
    },
    // 重置表单
    resetForm(formName) {
        this.$refs[formName].resetFields();
    }
  }
};
</script>

<style scoped>
</style>
