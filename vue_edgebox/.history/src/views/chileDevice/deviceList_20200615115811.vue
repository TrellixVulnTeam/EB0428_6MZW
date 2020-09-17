<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->  
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 操作 -->
    <el-row class="row-padding">
      <el-button size="small" :disabled="enableBtn" plain @click="chooseStatus_()">批量启用</el-button>
      <el-button size="small" :disabled="unableBtn" plain @click="chooseStatus_()">批量禁用</el-button>
      <el-button size="small" :disabled="deleteBtn" plain @click="enable_()">批量删除</el-button>
      <el-button type="primary" size="small" @click="dialogFormVisible = true"  >新 增</el-button>
      <el-button type="success" size="small" @click="flush_status" plain >刷 新</el-button>

      <el-input
        placeholder="请输入内容"
        size="small"
        v-model="searchDevice"
        class="pull-right search-input"
      >
        <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
    <el-row>
       <el-alert title="添加注册设备-->选择协议模板(配置采集信息)-->特征提取(关键字段)-->数据转发通道" type="success" show-icon></el-alert>
    </el-row>
    <!-- 子设备列表 -->
    <div v-loading="loading">
    <el-table
      :data="tableData"
      stripe
      ref="multipleTable"
      tooltip-effect="dark"
      :default-sort = "{prop: 'date', order: 'descending'}"
      :row-class-name="tableRowIndexArray"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" min-width="5%" ></el-table-column>
      <el-table-column label="名称" min-width="10%">
        <template v-slot="scope">
          <el-button type="text"  @click="getRowInfo(scope.row)">{{scope.row.subdevice_name}}</el-button>
        </template>
      </el-table-column>
      <el-table-column sortable min-width="13%" label="类型" prop="subdevice_type"></el-table-column>
      <el-table-column sortable min-width="10%" label="型号" prop="subdevice_model"></el-table-column>
      <el-table-column sortable label="位置" prop="subdevice_position" min-width="10%"></el-table-column>
      <!-- <el-table-column label="描述" prop="subdevice_remark"></el-table-column> -->
      <!-- <el-table-column
        label="最近上线时间"
        min-width='15%'>
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span >{{ scope.row.subdevice_online_time }}</span>
        </template>
      </el-table-column> -->
      <el-table-column sortable label="最近上线时间" prop="subdevice_online_time" min-width='15%'></el-table-column>
      <el-table-column sortable label="启用/禁用" min-width="11%">
        <template v-slot="scope">
          <el-tooltip placement="top">
            <div slot="content">点击启用禁用设备,不影响采集驱动<br/>当禁用设备后传输通道全部关闭</div>
            <el-switch  v-model="scope.row.subdevice_enable" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column sortable label="状态" prop="subdevice_status" min-width="15%">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.subdevice_status ==='采集驱动'" size="medium">{{ scope.row.subdevice_status }}</el-tag>
            <el-tag v-else-if="scope.row.subdevice_status ==='传输驱动'" type="success" size="medium">{{ scope.row.subdevice_status }}</el-tag>
            <el-tag v-else-if="scope.row.subdevice_status ==='采集驱动&传输驱动'" size="medium">{{ scope.row.subdevice_status }}</el-tag>
            <el-tag v-else size="medium" type="info">{{ scope.row.subdevice_status }}</el-tag>
          </template>
          
      </el-table-column>
      <el-table-column label="操作" min-width="10%">
        <template v-slot="scope">
          <el-button type="text"  @click="modifyFormInfo(scope.row)">修改</el-button>
          <el-button type="text" style="color: #FF0000" @click="deleteRow(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>
    <!-- 新增设备弹出框 -->
    <el-dialog title="添加子设备" :visible.sync="dialogFormVisible" custom-class="chile-device-box dialog-form" width="560px">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="所属类别:" prop="typeSelect">
          <el-select size="small" style="width: 100%" v-model="form.typeSelect" placeholder="请选择设备所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.value">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备名称:" prop="name">
          <el-input type="text" size="small" v-model="form.name" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="subdevice name :case HC001"></el-input>
        </el-form-item>  
        <el-form-item label="设备型号:" prop="model">
          <el-input type="text" size="small" v-model="form.model" placeholder="subdevicce model :case 惠测"></el-input>
        </el-form-item>
        <el-form-item label="设备位置:" prop="position">
          <el-input type="text" size="small" v-model="form.position" placeholder="subdevice position :case E5-4F"></el-input>
        </el-form-item>
        <el-form-item label="设备描述:" >
          <el-input type="textarea" rows="3" v-model="form.description" placeholder="sbdevice remark :case 这是一个惠测单相电表"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="resetForm('form')">重置</el-button>
        <el-button type="primary" size="small" @click="submitForm('form')">确定</el-button>
      </el-row>
    </el-dialog>
    <!-- 修改设备信息弹出框 -->
    <el-dialog title="修改子设备信息" :visible.sync="modifyDialog" custom-class="chile-device-box dialog-form"  width="560px">
      <el-form :model="modifyForm" label-position="left" label-width="100px" :rules="modifyrules" ref="modifyForm">
        
        <el-form-item label="设备名称:" prop="name">
          <el-input type="text" size="small" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" v-model="modifyForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="所属类别:" prop="typeSelect">
          <el-select size="small" style="width: 100%" v-model="modifyForm.typeSelect" placeholder="请选择所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备型号:" prop="model">
          <el-input type="text" size="small" v-model="modifyForm.model"></el-input>
        </el-form-item>
        <el-form-item label="设备位置:" prop="position">
          <el-input type="text" size="small" v-model="modifyForm.position"></el-input>
        </el-form-item>       
        <el-form-item label="设备描述:" >
          <el-input type="textarea" rows="3" v-model="modifyForm.description"></el-input>
        </el-form-item>
        
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="modifyDialog=false">取消</el-button>
        <el-button type="primary" size="small" @click="modify('modifyForm')">确定</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
import { checkNull } from '../../until/checkRules'
export default {
  data() {
    // 检测设备名是否已经被注册
      var duladevicename = (rule, value, callback) => {
        // 验证设备名是否存在.  一会再写
        if (value.length < 3) {
          callback(new Error('长度在 3 到 15 个字符之间'))
        } else if (value.length > 15) {
          callback(new Error('长度在 3 到 15 个字符之间'))
        } else {
          this.$axios.post('/apis/device/create?select=1', {
            select_devicename: value
          })
            .then(response => {
              if (response.data.is_indb === 1) {
                callback(new Error('该设备名已经存在！'))
              } else {
                callback();
              }
            })
        }
      }
    return {
      searchDevice: "", // 搜索设备名称
      tableData: [
        // {},
        // {}
        ], // 设备列表数据
      
      dialogFormVisible: false, // 弹出框控制
      loading: false,
      multipleSelection: [],
      form: { // 表单元素
          name: '',
          typeSelect: '',
          position: '',
          model: '',
          description: ''
      },
      
      typeList: [],// 设备类型列表 
      rules: { // 表单验证
          name: [
              { required: true, validator: checkNull, trigger: 'blur' },
              // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
              {validator: duladevicename, trigger: 'blur'}
          ],
          typeSelect: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
          position: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              },
              { min: 2, max: 15, message: '长度在 2 到 15 个字符之间', trigger: 'blur' }
          ],
          model: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              },
              { min: 2, max: 15, message: '长度在 2 到 15 个字符之间', trigger: 'blur' }
          ]
      },
      modifyrules: { // 表单验证
          typeSelect: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
          position: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              },
              { min: 2, max: 15, message: '长度在 2 到 15 个字符之间', trigger: 'blur' }
          ],
          model: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              },
              { min: 2, max: 15, message: '长度在 2 到 15 个字符之间', trigger: 'blur' }
          ]
      },
      delay: false,
      deleteBtn: true, // 批量删除按钮状态
      enableBtn: true, // 批量启用按钮状态
      unableBtn: true, // 批量禁用按钮状态
      enableRows: [], // 批量启用的数组数据
      unableRows: [], // 批量禁用的数组数据
      modifyDialog: false, // 修改子设备信息弹出框
      modifyForm: {  // 修改设备信息
        name: '',
        typeSelect: '',
        position: '',
        model: '',
        description: ''
      },
    };
  },
  created() {
    this.flush_status()
    this.loading = false;
    
  },
  methods: {
    flush_status: function () {
      this.loading = true,
      this.$axios.get("apis/device/list/")
        .then(response => {
          this.tableData = response.data.db;
        })
      this.$axios.get("apis/device/type/")
       .then(response => {
        this.typeList = response.data.db;
      })
      setTimeout(() => {
        this.loading = false;
      }, 300);
    },
    getRowInfo(row) {
      let subdevice_name = row.subdevice_name;
      let l = row;
      window.sessionStorage.setItem('pip_index', JSON.stringify("00"));
      window.sessionStorage.setItem('subdevice', JSON.stringify(subdevice_name));
      this.$router.push({path: 'deviceManage',query:{subdevice: l}});
    },
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
        if (selectRows[i].subdevice_enable == true) {
          enableBtn = true;
          break;
        } else {
          enableRows.push(selectRows[i]);
          enableBtn = false;
        }
      }
      // 筛选数据判断批量禁用按钮的状态
      for (let i in selectRows) {
        if (selectRows[i].subdevice_enable == false) {
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
    //  批量启用或者禁用
    chooseStatus_(){
      let selectRows = this.multipleSelection; 
      let subdevice_name_list = [];
      let enable = selectRows[0].subdevice_enable;
      for (let i in selectRows) {
        subdevice_name_list.push(selectRows[i].subdevice_name);
      }
      // console.log(subdevice_name_list)
      var _this = this;
      this.$axios.post('apis/device/enable?more=1', {
          subdevice_name_list: subdevice_name_list,
          enable: enable
        })
        .then(function (response) {
          _this.$Message.SuccessMessage(_this, response.data.message);
          _this.flush_status()
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    // 启用或者禁用
    chooseStatus(row) {
        var _this = this;
        this.$axios.post('apis/device/enable', {
              subdevice_name: row.subdevice_name,
              enable: row.subdevice_enable
            })
            .then(function (response) {
              _this.$Message.SuccessMessage(_this, response.data.message);
            })
            .catch(function (error) {
              console.log(error);
            });
    },
    // 删除数据
    deleteRow(rows) {
      this.$Message.WarningAlert(this,'您确定要删除此设备吗？','设备删除').then(
        res => {
          // console.log('1111');
          if(rows.subdevice_enable) {
            this.$Message.WarningAlert(this, "设备是启用状态不能删除！");
          }
          else{
            var _this = this;
            this.$axios.post('apis/device/delete', {
              subdevice_name: rows.subdevice_name,
            })
            .then(function (response) {
              console.log(response.data.message);
              _this.flush_status()
            })
            .catch(function (error) {
              console.log(error);
            });
          }
          
        }
      );
      
    },
    // 修改数据
    modify(formName) {
      var _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(222222);
          this.$axios.post('apis/device/create?update=1', {
            subdevice_name: this.modifyForm.name,
            subdevice_type: this.modifyForm.typeSelect,
            subdevice_position: this.modifyForm.position,
            subdevice_model: this.modifyForm.model,
            subdevice_remark: this.modifyForm.description
          })
          .then(function (response) {
            console.log(response.data.message);
            _this.modifyDialog = false
            _this.resetForm(formName);
            _this.form.description= "";
            _this.flush_status()
          })
          .catch(function (error) {
            console.log(error);
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    modifyFormInfo(rows) {
      this.modifyDialog = true;
      this.modifyForm = {
        name: rows.subdevice_name,
        typeSelect: rows.subdevice_type,
        position: rows.subdevice_position,
        model: rows.subdevice_model,
        description: rows.subdevice_remark

      }
    },
    // 提交表单
    submitForm(formName) {
      var _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/create/', {
          subdevice_name: this.form.name,
          subdevice_type: this.form.typeSelect,
          subdevice_position: this.form.position,
          subdevice_model: this.form.model,
          subdevice_remark: this.form.description
          })
          .then(function (response) {
            console.log(response.data.message);
            _this.dialogFormVisible = false
            _this.resetForm(formName);
            _this.form.description= "";
            _this.flush_status()
          })
          .catch(function (error) {
            console.log(error);
          });
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
