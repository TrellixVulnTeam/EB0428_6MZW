<template>
  <el-main class="no-padding">

    <el-row>
      <el-form :inline="true" v-loading="loading"  :model="selectProtocol" ref="selectProtocol">
        <el-form-item
          prop="typeSelected"
          :rules="[
              {  required: true, message: '请先选择设备协议名称!',trigger: 'blur',},
          ]"
        >
            <el-cascader
            :options="protocolList"
            :clearable="true"
            :show-all-levels="false"
            v-model="selectProtocol.typeSelected"
            size="small" placeholder="按协议名称查找模板"
            @change="catProtocolChange"></el-cascader>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small" @click="submitFormCreate('selectProtocol')"  >新增协议模板</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-table :data="templateListTable" ref="refTable"
    :default-sort = "{prop: 'date', order: 'descending'}"
    @row-click="clickTable">

        <el-table-column sortable label="模板名称" prop="name"></el-table-column>
        <el-table-column sortable label="创建时间" prop="create_time"></el-table-column>
         <el-table-column label="协议名称" prop="protocol">
          <template slot-scope="scope">
            <el-tag size="medium" type="success">{{ scope.row.protocol }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="80">
            <template v-slot="scope">
                <el-button v-if="scope.row.is_default === false" type="text" size="small" @click="templateApply(scope.row)">
                  <span v-if="scope.row.name === apply_status" >重新应用</span>
                  <span v-else>应用</span>
                </el-button>
                <!-- <el-button v-if="scope.row.is_default === false & scope.row.name === apply_status" type="text" size="small" @click="templateApply(scope.row)">
                  重新应用
                </el-button>
                 <el-button v-else-if="scope.row.is_default === false & scope.row.name !== apply_status" type="text" size="small" @click="templateApply(scope.row)">
                  应用
                </el-button> -->
                <el-tag v-else type="success">基模板</el-tag>
            </template>
        </el-table-column>
        <el-table-column type="expand"  >
            <template  v-slot="scope">
               <el-row  v-for="(key , i) in scope.row.info " :key ="Number(i)">
                  <el-col v-for="(val , j) in key " :key ="Number(j)" :span="6" >
                    <json-viewer
                      :value="val"
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

    <!-- 新增设备模板 TCP RTU 配置 -->
    <div class="dialogfrommodel">
      <el-dialog :title="'新增设备模板('+selectProtocol.typeSelected[1]+')'" :visible.sync="dialogFormCreate"  width= "800px">
        <el-form  label-position="top"  :model="dynamicValidateForm"  ref="dynamicValidateForm" inline-message= true>
          <el-table :data="dynamicValidateForm.domains" class="table" style="width: 100%">
            <el-table-column label="功能码" prop="function_code" min-width="10%">
                <template slot-scope="scope">
                    <el-form-item   :prop="'domains.' + scope.$index + '.function_code'"
                    :rules="[
                          { required: true, message: '必填!', trigger: ['blur','change'] },
                    ]">
                      <el-select size="small" v-model="scope.row.function_code" placeholder="03">
                        <el-option v-for="item in appforms.function_code" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="起始寄存器" prop="start_register" min-width="12%">
              <!-- <el-input size="small" ></el-input> -->
                <template slot-scope="scope">
                    <el-form-item   :prop="'domains.' + scope.$index + '.start_register'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]"
                    >
                      <el-input size="small" maxlength="4" oninput="value=value.replace(/[^0-9^A-F^a-f]/g, '')" v-model="scope.row.start_register" placeholder="0x0001" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="寄存器个数" prop="register_num" min-width="12%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.register_num'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small"  maxlength="4" oninput="value=value.replace(/[^0-9^A-F^a-f]/g, '')" v-model="scope.row.register_num" placeholder="0x0001" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="属性名" prop="property" min-width="18%">
                <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.property'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small" v-model="scope.row.property"  placeholder="property" ></el-input>
                      <!-- <el-input size="small" v-model="scope.row.property" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="property" ></el-input> -->
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="数据格式" prop="format" min-width="18%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.format'"
                    :rules="[
                          { required: true, message: '必填!', trigger: ['blur','change'] },
                    ]">
                      <el-select size="small" v-model="scope.row.format" placeholder="16进制输出">
                        <el-option v-for="item in appforms.format" :key="item.index" :label="item.value" :value="item.index">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label='规则计算' prop="rule" min-width="20%">
              <template slot-scope="scope"  >
                <el-form-item  :prop="'domains.' + scope.$index + '.rule'" >
                  <div v-if="scope.row.format === 1 || scope.row.format === 3 ">
                      <el-select size="small" style="width: 50px" v-model="scope.row.rule.sign" placeholder="+">
                      <el-option v-for="item in appforms.rule" :key="item.index" :label="item.value" :value="item.value">
                      </el-option>
                      </el-select>
                      <el-input size="small" type="number" style="width: 90px"  v-model="scope.row.rule.number" placeholder="100" ></el-input>
                  </div>
                  <div v-else >
                    <el-select size="small" disabled style="width: 50px" v-model="scope.row.rule.sign" placeholder="+">
                        <el-option v-for="item in appforms.rule" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                      <el-input  disabled size="small" oninput="value=value.replace(/[^\d]/g, '')" style="width: 90px" v-model="scope.row.rule.number" placeholder="100" ></el-input>
                  </div>

                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label='' prop="rule" min-width="8%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.property'" >
                      <el-button size= "small" type="danger" icon="el-icon-delete" @click="removeDomain(scope.row)" plain></el-button>
                    </el-form-item>
                </template>
            </el-table-column>
          </el-table>
        </el-form>
        <el-row  slot="footer">
          <el-button type="primary" @click="addDomain('dynamicValidateForm')" size="small" plain>新增属性</el-button>
          <el-button type="primary" @click="submitForm('dynamicValidateForm')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>

    <!-- 新增设备模板 SMT 配置 -->
    <div class="dialogfrommodelsmt">
      <el-dialog  :title="'新增设备模板('+selectProtocol.typeSelected[1]+')'" :visible.sync="dialogFormCreateSMT" width="800px" >
          <!-- SMT配置 -->
          <el-form  label-position="top"  :model="dynamicValidateForm"  ref="dynamicValidateFormSMT" inline-message= true>
            <el-tabs type="card">
              <el-tab-pane v-for="(item, key) in baseTemplate" :key="key" :label="key" :name="key.$index">
                <el-table :data="baseTemplate[key]">
                  <el-table-column sortable label="属性名" prop="parameter_name">
                    <template slot-scope="scope">
                      <el-form-item   :prop="key +'\'.' + scope.$index +'.parameter_name'">
                        <strong value="scope.row.parameter_name" readonly>
                          {{scope.row.parameter_name}}
                        </strong>
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column sortable label="重命名" prop="parameter_rename">
                    <template slot-scope="scope">
                      <el-form-item   :prop="key +'\'.' + scope.$index +'.parameter_rename'">
                        <el-input v-model="scope.row.parameter_rename" value="scope.row.parameter_rename">
                        </el-input>
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column sortable label="中文属性名" prop="parameter_name_ch">
                    <template slot-scope="scope">
                      <el-form-item   :prop="key +'\'.' + scope.$index +'.parameter_name_ch'">
                        <el-input v-model="scope.row.parameter_name_ch" value="scope.row.parameter_name_ch">
                        </el-input>
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column sortable label="数据类型" prop="parameter_type">
                    <template slot-scope="scope">
                      <el-form-item   :prop="key +'\'.' + scope.$index +'.parameter_type'">
                        <el-select v-model="scope.row.parameter_type" value="scope.row.parameter_type">
                            <el-option v-for="(item, i) in ['string', 'data', 'int', 'float']" :key="i" :label="item" :value="item">
                            </el-option>
                        </el-select>
                      </el-form-item>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </el-form>
          <el-card>
            <!-- <el-row  slot="footer"> -->
            <!-- <el-button type="primary" @click="addDomain('dynamicValidateForm')" size="small" plain>新增属性</el-button> -->
            <el-button type="primary" @click="submitForm('dynamicValidateFormSMT')" size="small">保存</el-button>
            <!-- </el-row> -->
          </el-card>
      </el-dialog>
    </div>

    <div class="dialogfrommodel1 dialogfrommodel">
      <el-dialog :title="'新增设备模板('+selectProtocol.typeSelected[1]+')'" :visible.sync="dialogFormCreateMQTT"  width= "680px">
        <el-form  label-position="left"  :model="mqttform"   ref="mqttform" inline-message= true>
          <el-table :data="mqttform.domains" class="table" style="width: 100%">
            <el-table-column label="字段名称" prop="property" min-width="22%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.property'" :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                  <el-input size="small"  v-model="scope.row.property" oninput="value=value.replace(/[^0-9/^A-Z^a-z]/g, '')" placeholder="property" ></el-input>
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="设置别名" prop="as_name" min-width="22%">
                <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.as_name'"
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small"  v-model="scope.row.as_name" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="as name" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="字段类型" prop="type" min-width="22%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.type'" >
                  <el-radio-group v-model="scope.row.type" size="small">
                    <el-radio-button label="root">根数据</el-radio-button>
                    <el-radio-button label="node">节点数据</el-radio-button>
                  </el-radio-group>
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="是否为空" prop="is_null" min-width="10%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.is_null'" >
                      <el-select size="small" v-model="scope.row.is_null" placeholder="是">
                        <el-option v-for="item in appforms.NULL_type" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>
            </el-table-column>

            <el-table-column label='' prop="as_name" min-width="8%">
              <template slot-scope="scope">
                  <el-button size= "small" type="danger" icon="el-icon-delete" @click="removemqttform(scope.row)" plain></el-button>
                </template>
            </el-table-column>

          </el-table>
       </el-form>
        <el-row  slot="footer">
          <el-button type="primary" @click="addDomain('mqttform')" size="small" plain>新增字段</el-button>
          <el-button type="primary" @click="submitForm('mqttform')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>

    <!-- 应用模板弹出框 -->
    <el-dialog :title="'协议接口配置('+select_template+')'" :visible.sync="dialogFormRtu" width="680px" custom-class="chile-device-box dialog-form" >
      <modbus-rtu-form  :template_name ="select_template"
        @CloseDialog="closeDialogRtu" >
      </modbus-rtu-form>
    </el-dialog>
    <el-dialog :title="'协议接口配置('+select_template+')'" :visible.sync="dialogFormSMT" width="680px" custom-class="chile-device-box dialog-form">
      <smt-form  :template_name ="select_template" :device_type="protocol" :file_type="file_type" :category="category"
        @CloseDialog="closeDialogSmt" >
      </smt-form>

    </el-dialog>
     <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormTcp" width="680px" custom-class="chile-device-box dialog-form"
    >
      <modbus-tcp-form  :template_name ="select_template"
        @CloseDialog="closeDialogTcp" >
      </modbus-tcp-form>

    </el-dialog>
    <div class="dialogFormtemplate">
    <el-dialog title="模板保存" :visible.sync="dialogFormCreatedesc" width="560px">
      <el-radio-group v-model="templateForm.type" size="small">
        <el-radio-button label="template">保存至通用模板库(默认)</el-radio-button>
        <el-radio-button label="one">不保存,只对该设备可用</el-radio-button>
      </el-radio-group>
      <div style="margin: 20px;"></div>
      <el-form  label-position="left" label-width="100px" :model="templateForm" :rules="tmp_rules"  ref="templateForm">
        <el-form-item
          class = "el-form-item1"
          prop="name"
          label="模板名"
        >
          <el-input v-model="templateForm.name" placeholder="template name"></el-input>
      </el-form-item>
      <el-form-item
          class = "el-form-item1"
          prop="description"
          label="模板描述"
        >
          <el-input v-model="templateForm.description" placeholder="template desc"></el-input>
      </el-form-item>
      </el-form>
       <el-row  slot="footer">
        <el-button type="primary" @click="dialogFormCreatedesc = false" size="small" plain>取消</el-button>
        <el-button type="primary"  size="small" @click="saveTemplate('templateForm')">确认</el-button>
      </el-row>
    </el-dialog>
    </div>
  </el-main>
</template>

<script>
import { checkNull } from '../../../until/checkRules'
import modbusRtuForm from '../components/modbusRtuForm.vue'
import modbusTcpForm from '../components/modbusTcpForm.vue'
import smtForm from '../components/smtForm.vue'

export default {
  data () {
    // 检测模板名是否已经存在
    var dulatemplateName = (rule, value, callback) => {
      // 验证用户名是否存在.  一会再写
      if (value.length < 2) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else if (value.length > 15) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else {
        callback()
      }

      // } else {
      //   this.$axios.post('/apis/device/template?select=1', {
      //     select_template_name: value,
      //     type: this.selectProtocol.typeSelected
      //   })
      //     .then(response => {
      //       if (response.data.is_indb === 1) {
      //         callback(new Error('该模板名称已经存在！'))
      //       } else {
      //         callback()
      //       }
      //     })
      // }
    }
    return {
      apply_status: false,
      collect_enable: false,
      sub_device_name: JSON.parse(sessionStorage.getItem('sub_device_name')),
      tmp_rules: { // 表单验证
        template_name: [
          { required: true, message: '请输入设备模板名称!', trigger: 'blur' },
          { validator: dulatemplateName, trigger: 'blur' }
        ],
        remark: [
          { required: true, message: '请输入该设备模板的描述信息!', trigger: 'blur' },
          { min: 5, max: 30, message: '长度在 5 到 30 个字符之间', trigger: 'blur' }
        ]
      },
      baseTemplate: {},
      appforms: {
        function_code: [
          { index: 0, value: '03' },
          { index: 1, value: '04' }
        ],
        format: [
          { index: 0, value: '2进制输出' },
          { index: 1, value: '10进制输出' },
          { index: 2, value: '16进制输出' },
          { index: 3, value: 'IEEE-754输出' },
          { index: 4, value: 'DATA-2301输出' },
          { index: 5, value: '浮点型输出' }

        ],
        NULL_type: [
          { index: 0, value: '是' },
          { index: 1, value: '否' }
        ],
        rule: [
          { index: 0, value: '+' },
          { index: 1, value: '-' },
          { index: 2, value: '*' },
          { index: 3, value: '/' }
        ]
      },
      dynamicValidateForm: {
        protocol: 'modbus_rtu',
        domains: [{
          function_code: '',
          start_register: '',
          register_num: '',
          property: '',
          format: '',
          rule: {
            sign: '',
            number: ''
          }
        }]

      },
      dynamicValidateFormSMT: {},
      mqttform: {
        domains: [{
          property: '',
          type: 'root',
          is_null: '是',
          as_name: ''
        }] },
      templateForm: {
        name: '',
        description: '',
        type: 'template'
      },
      dialogFormCreateSMT: false,
      dialogFormCreate: false,
      dialogFormCreateMQTT: false,
      dialogFormCreatedesc: false,
      loading: false,
      select_template: '',
      category: '',
      protocol: '',
      file_type: '',
      selectProtocol: {
        typeSelected: ''
      },

      protocolList: [],
      templateListTable: [{
        name: '',
        protocol: '',
        create_time: '',
        description: '',
        file_type: ''
      }],
      // dialogFormVisible: false,
      dialogFormTcp: false,
      dialogFormRtu: false,
      dialogFormSMT: false,
      rules: {
        typeSelected: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          }
        ]
      }
    }
  },
  components: {
    modbusRtuForm,
    modbusTcpForm,
    smtForm
  },
  created () {
    this.getProtocolTemplate()
  },
  methods: {
    templateApply (row) {
      if (this.collect_enable === true) {
        this.$Message.ErrorMessage(this, '请先禁用设备采集驱动再重新应用模板！')
        return
      }
      this.protocol = row.protocol
      this.select_template = row.name
      this.file_type = row.file_type
      this.category = row.category
      switch (this.category) {
        case 'Modbus-TCP':
          this.dialogFormTcp = true
          break
        case 'Modbus-RTU':
          this.dialogFormRtu = true
          break
        case 'SMT':
          this.dialogFormSMT = true
          break
      }
    },
    clickTable (row, index, e) {
      this.$refs.refTable.toggleRowExpansion(row)
    },
    catProtocolChange () {
      var _this = this
      if (this.selectProtocol.typeSelected.length === 0) {
        _this.getProtocolTemplate()
      } else {
        this.$axios.get('apis/device/template/search', {
          params: {
            typeSelected: this.selectProtocol.typeSelected
          }
        })
          .then(response => {
            if (response.data.status_code === 0) {
              _this.templateListTable = response.data.template_list
              _this.baseTemplate = response.data.base_template
              _this.dynamicValidateFormSMT = _this.baseTemplate
            } else {
              _this.$Message.ErrorMessage(response.data.message)
            }
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    getProtocolTemplate () {
      var _this = this
      _this.$axios.get('apis/device/protocol/') // 设备协议清单
        .then(response => {
          _this.protocolList = response.data.protocol_list
        })
      _this.$axios.get('apis/device/getTemplate', {
        params: {
          sub_device_name: _this.sub_device_name
        }
      })
        .then(response => {
          if (response.data.status_code === 0) {
            _this.templateListTable = response.data.template_list
            _this.collect_enable = response.data.collect_enable
            _this.apply_status = response.data.apply_status
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    closeDialogTcp (val) {
      this.dialogFormTcp = val
      this.$emit('dump')
      // this.selectProtocol.typeSelected=""
    },
    closeDialogRtu (val) {
      this.dialogFormRtu = val
      this.$emit('dump')
    },
    closeDialogSmt (val) {
      this.dialogFormSMT = val
      this.$emit('dump')
    },
    saveTemplate (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/template/create/', {
            template_info: this.dynamicValidateFormSMT,
            name: this.templateForm.name,
            description: this.templateForm.description,
            type: this.templateForm.type,
            selects: this.selectProtocol.typeSelected
          })
            .then(function (response) {
              if (response.data.status_code === 0) {
                _this.$Message.SuccessMessage(_this, response.data.message)
                _this.resetForm(formName)
                _this.resetForm('dynamicValidateFormSMT')
                _this.dialogFormCreateSMT = false
                _this.dialogFormCreatedesc = false
              } else {
                _this.$Message.ErrorMessage(_this, response.data.message)
              }
            })
            .catch(function (error) {
              alert(error)
            })
          setTimeout(() => {
            this.$axios.get('apis/device/template/search', {
              params: {
                typeSelected: this.selectProtocol.typeSelected
              }
            }).then(response => {
              _this.templateListTable = response.data.template_list
            })
              .catch(function (error) {
                console.log(error)
              })
          }, 300)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(formName)
          this.dialogFormCreatedesc = true
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    submitFormCreate (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          switch (this.selectProtocol.typeSelected[1]) {
            case 'SMT':
              this.dialogFormCreateSMT = true
              break
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.dynamicValidateForm = {
        domains: [{
          function_code: '',
          start_register: '',
          register_num: '',
          property: '',
          format: '',
          rule: {
            sign: '',
            number: ''
          }
        }],
        template_name: '',
        remark: ''
      }
    },
    removemqttform (item) {
      var index = this.mqttform.domains.indexOf(item)
      if (this.mqttform.domains.length !== 1) {
        this.mqttform.domains.splice(index, 1)
      }
    },
    removeDomain (item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (this.dynamicValidateForm.domains.length !== 1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (formName === 'mqttform') {
            this.mqttform.domains.push(
              {
                property: '',
                type: 'root',
                is_null: '是',
                as_name: ''
              }
            )
          } else if (formName === 'dynamicValidateForm') {
            this.dynamicValidateForm.domains.push({
              function_code: this.dynamicValidateForm.domains[0].function_code,
              start_register: '',
              register_num: '',
              property: '',
              format: '',
              rule: {
                sign: '',
                number: ''
              }
            })
          }
        } else {
          console.log('no add!!')
          return false
        }
      })
    }
  }

}
</script>

<style >
.dialogFormtemplate .el-dialog__body{
   padding: 20px 20px 0px;
}
.dialogfrommodel .el-dialog__body {
  padding: 10px 20px
}
.dialogfrommodel .el-table .cell {
  padding-left: 0px;
}
.dialogfrommodel .el-form-item {
  margin-bottom: 0px
}
.dialogfrommodel .el-form-item1 {
  margin-bottom: 20px;

}

.el-table__expanded-cell[class*=cell] {
   padding: 20px 30px;
   background-color: #1e466b21;
}
.el-col-6 {
  padding: 7px;
}
.el-input__inner {
  padding: 0 4px;
}
.dialog-form .el-dialog__body {
    padding: 10px 20px 15px 20px;
}
.dialogfrommodel .el-radio-button__orig-radio:checked+.el-radio-button__inner {
    color: #FFF;
    background-color: #08c78f;
    border-color: #08c78f;
    -webkit-box-shadow: -1px 0 0 0 #08c78f;
    box-shadow: -1px 0 0 0 #08c78f;
}
</style>
