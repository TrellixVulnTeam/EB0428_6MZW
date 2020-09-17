<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">子设备列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 操作 -->
    <el-row class="row-padding">
      <el-button size="small" :disabled="enableBtn" plain @click="batchEnable(true)">批量启用</el-button>
      <el-button size="small" :disabled="disabledBtn" plain @click="batchEnable(false)">批量禁用</el-button>
      <el-button size="small" :disabled="deleteBtn" plain @click="bulkDelete()">批量删除</el-button>
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
      <el-table-column type="selection" min-width="2%" ></el-table-column>
      <el-table-column label="名称" min-width="20%">
        <template v-slot="scope">
          <el-button type="text"  @click="getRowInfo(scope.row)">{{scope.row.sub_device_name}}</el-button>
        </template>
      </el-table-column>
      <el-table-column sortable min-width="13%" label="类型" prop="category"></el-table-column>
      <el-table-column sortable min-width="13%" label="厂商" prop="firm"></el-table-column>
      <el-table-column sortable min-width="10%" label="型号" prop="model"></el-table-column>
      <el-table-column sortable label="位置" prop="position" min-width="10%"></el-table-column>
      <!-- <el-table-column label="描述" prop="subdevice_remark"></el-table-column> -->
      <!-- <el-table-column
        label="最近上线时间"
        min-width='15%'>
        <template slot-scope="scope">
          <i class="el-icon-time"></i>
          <span >{{ scope.row.subdevice_online_time }}</span>
        </template>
      </el-table-column> -->
      <el-table-column sortable label="最近上线时间" prop="last_online_time" min-width='15%'></el-table-column>
      <el-table-column sortable label="启用/禁用" prop="enable" min-width="11%">
        <template v-slot="scope">
          <el-tooltip placement="top">
            <div slot="content">点击启用禁用设备,不影响采集驱动<br/>当禁用设备后传输通道全部关闭</div>
            <el-switch  v-model="scope.row.enable" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column sortable label="在线状态" prop="status" min-width="15%">
          <template slot-scope="scope">
            <el-tag  v-if="scope.row.status === true" type="success" size="medium">在线</el-tag>
            <el-tag v-else type="primary" size="medium">离线</el-tag>
            <!-- <el-tag v-else-if="scope.row.subdevice_status ==='传输驱动'" type="success" size="medium">{{ scope.row.subdevice_status }}</el-tag>
            <el-tag v-else-if="scope.row.subdevice_status ==='采集驱动&传输驱动'" size="medium">{{ scope.row.subdevice_status }}</el-tag>
            <el-tag v-else size="medium" type="info">{{ scope.row.subdevice_status }}</el-tag> -->
          </template>

      </el-table-column>
      <el-table-column sortable label="驱动状态" prop="drive_status" min-width="15%">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.drive_status !=='暂无驱动'" type="success" size="medium">{{ scope.row.drive_status }}</el-tag>
            <el-tag v-else type="primary" size="medium">{{ scope.row.drive_status }}</el-tag>
          </template>
      </el-table-column>
      <el-table-column label="操作" min-width="10%">
        <template v-slot="scope">
          <el-button type="text"  @click="modifyFormInfo(scope.row)">修改</el-button>
          <el-button type="text" style="color: #FF0000" @click="deleteRow(scope.row)">删除</el-button>
        </template>
      </el-table-column>
      <el-table-column type="expand" prop="description">
        <template slot-scope="scope">
            <el-row>
              描述<el-input  type="text" size="medium" :value="scope.row.description" readonly></el-input>
            </el-row>
        </template>
      </el-table-column>
    </el-table>
    </div>
    <!-- 新增设备弹出框 -->
    <el-dialog title="添加子设备" :visible.sync="dialogFormVisible" custom-class="chile-device-box dialog-form" width="560px">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="所属类别:" prop="category">
          <el-select size="small" style="width: 100%" v-model="form.category" placeholder="请选择设备所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备名称:" prop="sub_device_name">
          <el-input type="text" size="small" v-model="form.sub_device_name" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="subdevice name :case HC001"></el-input>
        </el-form-item>
         <el-form-item label="设备厂商:" prop="firm">
          <el-input type="text" size="small" v-model="form.firm"  placeholder="sub_device_firm :case 惠测"></el-input>
        </el-form-item>
        <el-form-item label="设备型号:" prop="model">
          <el-input type="text" size="small" v-model="form.model" placeholder="sub_device_model :case HC33A"></el-input>
        </el-form-item>
        <el-form-item label="设备位置:" prop="position">
          <el-input type="text" size="small" v-model="form.position" placeholder="sub_device_position :case E5-4F"></el-input>
        </el-form-item>
        <el-form-item label="设备描述:" >
          <el-input type="textarea" rows="3" v-model="form.description" placeholder="sub_device_description :case 这是一个惠测三相电表"></el-input>
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
        <el-form-item label="设备名称:" prop="sub_device_name">
          <el-input type="text" size="small" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" v-model="modifyForm.sub_device_name" disabled></el-input>
        </el-form-item>
        <el-form-item label="所属类别:" prop="typeSelect">
          <el-select size="small" style="width: 100%" v-model="modifyForm.category" placeholder="请选择所属类别">
            <el-option v-for="item in typeList" :key="item.index" :label="item.value" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备厂商:" prop="model">
          <el-input type="text" size="small" v-model="modifyForm.firm"></el-input>
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
  data () {
    // 检测设备名是否已经被注册
    var duladevicename = (rule, value, callback) => {
      // 验证设备名是否存在.  一会再写
      if (value.length < 3) {
        callback(new Error('长度在 3 到 15 个字符之间'))
      } else if (value.length > 15) {
        callback(new Error('长度在 3 到 15 个字符之间'))
      } else {
        this.$axios.post('/apis/device/create?select=1', {
          sub_device_name: value
        })
          .then(response => {
            if (response.data.is_indb === 1) {
              callback(new Error('该设备名已经存在！'))
            } else {
              callback()
            }
          })
      }
    }
    return {
      searchDevice: '', // 搜索设备名称
      tableData: [
        // {},
        // {}
      ], // 设备列表数据

      dialogFormVisible: false, // 弹出框控制
      loading: false,
      multipleSelection: [],
      form: { // 表单元素
        sub_device_name: 'SMT',
        category: 'SMT设备类',
        position: 'E5-4F',
        firm: 'TRI',
        model: 'TRI_7007_SPI',
        description: 'TRI_7007_SPI'
      },

      typeList: [], // 设备类型列表
      rules: { // 表单验证
        name: [
          { required: true, validator: checkNull, trigger: 'blur' },
          // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
          { validator: duladevicename, trigger: 'blur' }
        ],
        typeSelect: [
          {
            required: false, validator: checkNull, trigger: 'blur'
          }
        ],
        position: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          },
          { min: 2, max: 15, message: '长度在 2 到 15 个字符之间', trigger: 'blur' }
        ],
        firm: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          }
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
        firm: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          }
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
      disabledBtn: true, // 批量禁用按钮状态
      modifyDialog: false, // 修改子设备信息弹出框
      modifyForm: { // 修改设备信息
        sub_device_name: '',
        category: '',
        position: '',
        firm: '',
        model: '',
        description: ''
      }
    }
  },
  created () {
    this.flush_status()
    this.loading = false
  },
  methods: {
    flush_status: function () {
      this.loading = true
      this.$axios.get('apis/device/list/')
        .then(response => {
          this.tableData = response.data.db
        })
      this.$axios.get('apis/device/category/')
        .then(response => {
          this.typeList = response.data.db // TODO
        })
      setTimeout(() => {
        this.loading = false
      }, 300)
    },
    getRowInfo (row) {
      let subDeviceName = row.sub_device_name
      let l = row
      window.sessionStorage.setItem('pip_index', JSON.stringify('00'))
      window.sessionStorage.setItem('sub_device_name', JSON.stringify(subDeviceName))
      this.$router.push({ path: 'deviceManage', query: { sub_device_name: l } })
    },
    toggleSelection (rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row)
        })
      } else {
        this.$refs.multipleTable.clearSelection()
      }
    },
    tableRowIndexArray (row) {
      // 设置row对象的index
      row.row.index = row.rowIndex
    },
    handleSelectionChange (val) {
      this.multipleSelection = val
      console.log(val)
      // 判断批量删除按钮的状态
      this.deleteBtn = this.multipleSelection.length <= 0
      this.enableBtn = this.multipleSelection.length <= 0
      this.disabledBtn = this.multipleSelection.length <= 0
    },

    //  批量启用或者禁用
    batchEnable (enable) {
      var _this = this
      let selectRows = this.multipleSelection
      let subDeviceNameList = []
      for (let i in selectRows) {
        if (enable) {
          if (selectRows[i].enable === false) {
            subDeviceNameList.push(selectRows[i].sub_device_name)
          }
        } else {
          if (selectRows[i].enable === true) {
            subDeviceNameList.push(selectRows[i].sub_device_name)
          }
        }
      }
      if (enable) {
        if (subDeviceNameList !== undefined & subDeviceNameList.length > 0) {
        } else {
          _this.$Message.ErrorMessage(_this, '已全部启用')
          return
        }
      } else {
        if (subDeviceNameList !== undefined & subDeviceNameList.length > 0) {
        } else {
          _this.$Message.ErrorMessage(_this, '已全部禁用')
          return
        }
      }

      // console.log(subdevice_name_list)
      this.$axios.post('apis/device/enable', {
        sub_device_name_list: subDeviceNameList,
        enable: enable
      })
        .then(function (response) {
          if (response.data.status_code === 0) {
            _this.$Message.SuccessMessage(_this, response.data.message)
            _this.flush_status()
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
          }
        }
        )
        .catch(function (error) {
          console.log(error)
        })
    },
    // 批量删除
    bulkDelete () {
      var _this = this
      let selectRows = this.multipleSelection
      let subDeviceNameList = []
      let enableDeviceList = []
      for (let i in selectRows) {
        if (selectRows[i].enable) {
          enableDeviceList.push(selectRows[i].sub_device_name)
        } else {
          subDeviceNameList.push(selectRows[i].sub_device_name)
        }
      }
      // console.log(subdevice_name_list)
      if (subDeviceNameList !== undefined & subDeviceNameList.length > 0) {
        this.$Message.WarningAlert(this, '您确定要删除设备' + JSON.stringify(subDeviceNameList) + '吗？', '设备删除').then(
          res => {
            this.$axios.post('apis/device/delete', {
              sub_device_name_list: subDeviceNameList
            })
              .then(function (response) {
                if (response.data.status_code === 0) {
                  _this.$Message.SuccessMessage(_this, response.data.message)
                  _this.flush_status()
                } else {
                  _this.$Message.ErrorMessage(_this, response.data.message)
                }
              }
              )
              .catch(function (error) {
                console.log(error)
              })
          }
        )
      }
      setTimeout(() => {
        if (enableDeviceList !== undefined & enableDeviceList.length > 0) {
          this.$Message.WarningAlert(this, JSON.stringify(enableDeviceList) + '启用中不可删除')
        }
      }, 300)
    },
    // 启用或者禁用
    chooseStatus (row) {
      var _this = this
      this.$axios.post('apis/device/enable', {
        sub_device_name_list: [row.sub_device_name],
        enable: row.enable
      })
        .then(function (response) {
          _this.$Message.SuccessMessage(_this, response.data.message)
        })
        .catch(function (error) {
          console.log(error)
        })
      setTimeout(
        this.flush_status, 300
      )
    },
    // 删除数据
    deleteRow (row) {
      this.$Message.WarningAlert(this, '您确定要删除此设备吗？', '设备删除').then(
        res => {
          if (row.enable) {
            this.$Message.WarningAlert(this, '设备是启用状态不能删除！')
          } else {
            var _this = this
            this.$axios.post('apis/device/delete', {
              sub_device_name_list: [row.sub_device_name]
            })
              .then(function (response) {
                if (response.data.status_code === 0) {
                  _this.$Message.SuccessMessage(_this, response.data.message)
                  _this.flush_status()
                } else {
                  _this.$Message.ErrorMessage(_this, response.data.message)
                }
              })
              .catch(function (error) {
                console.log(error)
              })
          }
        }
      )
    },
    // 修改数据
    modify (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/modify', {
            sub_device_name: this.modifyForm.sub_device_name,
            category: this.modifyForm.category,
            position: this.modifyForm.position,
            firm: this.modifyForm.firm,
            model: this.modifyForm.model,
            description: this.modifyForm.description
          })
            .then(function (response) {
              if (response.data.status_code === 0) {
                _this.$Message.SuccessMessage(_this, response.data.message)
                _this.modifyDialog = false
                _this.resetForm(formName)
                _this.flush_status()
              } else {
                _this.$Message.ErrorMessage(_this, response.data.message)
              }
            })
            .catch(function (error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    modifyFormInfo (row) {
      this.modifyDialog = true
      this.modifyForm = {
        sub_device_name: row.sub_device_name,
        category: row.category,
        position: row.position,
        firm: row.firm,
        model: row.model,
        description: row.description
      }
    },
    // 提交表单
    submitForm (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/create/', {
            sub_device_name: this.form.sub_device_name,
            category: this.form.category,
            position: this.form.position,
            firm: this.form.firm,
            model: this.form.model,
            description: this.form.description
          })
            .then(function (response) {
              if (response.data.status_code === 0) {
                console.log(response.data.message)
                _this.$Message.SuccessMessage(_this, response.data.message)
                _this.dialogFormVisible = false
                _this.resetForm(formName)
                _this.flush_status()
              } else {
                _this.$Message.ErrorMessage(_this, response.data.message)
              }
            })
            .catch(function (error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 重置表单
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style scoped>
</style>
