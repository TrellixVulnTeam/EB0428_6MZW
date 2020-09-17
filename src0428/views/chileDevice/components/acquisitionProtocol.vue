<template>
  <el-main class="no-padding">
    
    <el-row>
      <el-form :inline="true" v-loading="loading"  :model="form1" ref="form1">
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
            v-model="form1.typeSelected" 
            size="small" placeholder="按协议名称查找模板"
            @change="catchange"></el-cascader>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small" @click="submitFormCreate('form1')"  >新增协议模板</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-table :data="tableData" ref="refTable" 
    :default-sort = "{prop: 'date', order: 'descending'}"
    @row-click="clickTable">
        
        <el-table-column sortable label="模板名称" prop="name"></el-table-column>
       
        <!-- <el-table-column
          label="创建时间"
          sortable>
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span >{{ scope.row.createTime }}</span>
          </template>
        </el-table-column> -->
        <el-table-column sortable label="创建时间" prop="createTime"></el-table-column>
         <el-table-column label="协议名称" prop="protocol">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.protocol === 'Modbus-RTU'" size="medium">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else-if="scope.row.protocol === 'Modbus-TCP'" size="medium" type="success">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else-if="scope.row.protocol === 'Canis Pro采集卡'" size="medium" type="warning">{{ scope.row.protocol }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="80">
            <template v-slot="scope">
                <el-button type="text" size="small" @click="templateApply(scope.row)">
                  <span v-if="form1.typeSelected === '' && tableData.length === 1">重新应用</span>
                  <span v-else-if="form1.typeSelected !==''">应用</span>
                </el-button>
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
      <el-dialog   :title="'新增设备模板('+form1.typeSelected[1]+')'" :visible.sync="dialogFormCreate"  width= "800px">
        <el-form  label-position="top"  :model="dynamicValidateForm"  ref="dynamicValidateForm" inline-message= true	>
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
          <el-button type="primary" @click="templateForm.templatetype='modbus'; submitForm('dynamicValidateForm')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>
    <div class="dialogfrommodel1 dialogfrommodel">
      <el-dialog   :title="'新增设备模板('+form1.typeSelected[1]+')'" :visible.sync="dialogFormCreateCanisPro"  width= "680px">
        <el-form  label-position="left"  :model="canisproform"   ref="canisproform" inline-message= true>
          <el-table :data="canisproform.domains" class="table" style="width: 100%">
            <el-table-column label="通道" prop="pip_no" min-width="10%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.pip_no'" :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                    <el-select size="small" v-model="scope.row.pip_no" placeholder="03">
                        <el-option v-for="item in appforms.pip_no" :key="item.index" :label="item.value" :value="item.index">
                        </el-option>
                    </el-select>
                  <!-- <el-input size="small"  v-model="scope.row.property" oninput="value=value.replace(/[^0-9/^A-Z^a-z]/g, '')" placeholder="property" ></el-input> -->
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="列名" prop="col" min-width="22%">
                <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.col'" 
                    :rules="[
                          { required: true, message: '必填!', trigger: 'blur' },
                    ]">
                      <el-input size="small"  v-model="scope.row.col" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="Sensor1" ></el-input>
                    </el-form-item>
                </template>
            </el-table-column>
            <el-table-column label="数据类型" prop="dtype" min-width="22%" >
              <template slot-scope="scope">
                <el-form-item  :prop="'domains.' + scope.$index + '.type'" >
                  <el-select size="small" v-model="scope.row.dtype" placeholder="数据类型">
                        <el-option v-for="item in appforms.dtype" :key="item.index" :label="item.value" :value="item.index">
                        </el-option>
                    </el-select>
                </el-form-item>
              </template>
            </el-table-column>
            <el-table-column label="精确值" prop="round" min-width="15%">
              <template slot-scope="scope">
                    <el-form-item  :prop="'domains.' + scope.$index + '.is_null'" >
                      <el-select size="small" v-model="scope.row.round" placeholder="是">
                        <el-option v-for="item in appforms.round" :key="item.index" :label="item.value" :value="item.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                </template>          
            </el-table-column>
            
            <el-table-column label=''  min-width="8%">
              <template slot-scope="scope">
                  <el-button size= "small" type="danger" icon="el-icon-delete" @click="removecanisproform(scope.row)" plain></el-button>
                </template>
            </el-table-column>
          
          </el-table>
       </el-form>
        <el-row  slot="footer">
          <el-button type="primary" @click="addDomain('canisproform')" size="small" plain>新增字段</el-button>
          <el-button type="primary" @click="templateForm.templatetype='canispro'; submitForm('canisproform')" size="small">保存</el-button>
        </el-row>
      </el-dialog>
    </div>
     <div class="dialogfrommodel">
      <el-dialog   :title="'新增设备模板('+form1.typeSelected[1]+')'" :visible.sync="dialogFormCreateMQTT"  width= "680px">
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
    <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormRtu" width="680px" custom-class="chile-device-box dialog-form"
    >
      <modbus-rtu-form  :templatename ="select_template"
        @CloseDialog="closeDialogRtu" >
      </modbus-rtu-form> 

    </el-dialog>
     <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormTcp" width="680px" custom-class="chile-device-box dialog-form"
    >
      <modbus-tcp-form  :templatename ="select_template"
        @CloseDialog="closeDialogTcp" >
      </modbus-tcp-form> 

    </el-dialog>
    <el-dialog :title="'协议接口配置('+select_template+')'"
        :visible.sync="dialogFormCanis" width="680px" custom-class="chile-device-box dialog-form"
    >
      <canis-pro-form  :templatename ="select_template"
        @CloseDialog="closeDialogCanis" >
      </canis-pro-form> 

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
          prop="template_name"
          label="模板名"
        >
          <el-input v-model="templateForm.template_name" placeholder="template name"></el-input>
      </el-form-item>
      <el-form-item
          class = "el-form-item1"                                                                                        
          prop="remark"
          label="模板描述"
        >
          <el-input v-model="templateForm.remark" placeholder="template desc"></el-input>
      </el-form-item>
      </el-form>
       <el-row  slot="footer">
        <el-button type="primary" @click="dialogFormCreatedesc = false" size="small" plain>取消</el-button>
        <el-button type="primary"  size="small" @click="saveTemp('templateForm')">确认</el-button>
      </el-row>
    </el-dialog>
    </div>
  </el-main>
</template>

<script>
import { checkNull } from '../../../until/checkRules';
import modbusRtuForm from '../components/modbusRtuForm.vue';
import modbusTcpForm from '../components/modbusTcpForm.vue';
import canisProForm from '../components/CanisProForm.vue'

export default {
  data() {
    // 检测模板名是否已经存在
      var dulatemplatename = (rule, value, callback) => {
        // 验证用户名是否存在.  一会再写
        if (value.length < 2) {
          callback(new Error('长度在 2 到 15 个字符之间'))
        } else if (value.length > 15) {
          callback(new Error('长度在 2 到 15 个字符之间'))
        } else {
          this.$axios.post('/apis/device/template?select=1', {
            select_templatename: value,
            type: this.form1.typeSelected[1],
          })
            .then(response => {
              if (response.data.is_indb === 1) {
                callback(new Error('该模板名称已经存在！'))
              } else {
                callback();
              }
            })
        }
      }
    return {
      drive_status: false,
      // dialogname: "",
      subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
      tmp_rules: { // 表单验证
          template_name: [
            { required: true, message: '请输入设备模板名称!', trigger: 'blur' },
            { validator: dulatemplatename, trigger: 'blur'}
          ],
          remark: [
            { required: true, message: '请输入该设备模板的描述信息!', trigger: 'blur' },
             { min: 5, max: 30, message: '长度在 5 到 30 个字符之间', trigger: 'blur' }
          ],
      },
      appforms: {
        pip_no: [
          { index: 0, value: '01'},
          { index: 1, value: '02'},
          { index: 2, value: '03'},
          { index: 3, value: '04'},
          { index: 4, value: '05'},
          { index: 5, value: '06'},

        ],
        function_code: [
          { index: 0, value: '03'},
          { index: 1, value: '04'},
        ],
        format: [
          { index: 0, value: '2进制输出'},
          { index: 1, value: '10进制输出'},
          { index: 2, value: '16进制输出'},
          { index: 3, value: 'IEEE-754输出'},
          { index: 4, value: 'DATA-2301输出'},
          { index: 5, value: '浮点型输出'},

        ],
        NULL_type: [
          { index: 0, value: '是'},
          { index: 1, value: '否'},
        ],
        dtype:[
          { index: 0, value: '电压值'},
        ],
        round: [
          { index: 0, value: 'e-6'}
        ],
        rule: [
          { index: 0, value: "+"},
          { index: 1, value: "-"},
          { index: 2, value: "*"},
          { index: 3, value: "/"},
        ]
      },
      dynamicValidateForm: {
          domains: [{
            function_code: '',
            start_register: '',
            register_num: '',
            property: '',
            format: '',
            rule: {
              sign : "",
              number: ""
            },            
          }],
      
      },
      canisproform: {
        domains: [{
          pip_no: "",
          col: "Sensor1",
          dtype:'',
          round: 'e-6'
        }]},
      mqttform: {
        domains: [{
          property: "",
          type: "root",
          is_null:'是',
          as_name: ''
        }]},
      templateForm: {
        template_name: '',
        remark: "",
        type: "template",
        template_type: ""
      },
      dialogFormCreate: false,
      dialogFormCreateMQTT: false,
      dialogFormCreateCanisPro: false,
      dialogFormCreatedesc:false,
      loading: false,
      select_template:'',
      form1:{
        typeSelected:"",
      },
    
      protocolList: [],
      tableData: [],
      // dialogFormVisible: false,
      dialogFormTcp: false,
      dialogFormRtu: false,
      dialogFormCanis: false,
      rules: {
        typeSelected: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
      },
    };  
  },
  components: {
    modbusRtuForm,
    modbusTcpForm,
    canisProForm,
  },
  created() {
    this.getData();
  },
  methods: {
    templateApply(row) {
      if(this.drive_status === true){
        this.$Message.ErrorMessage(this, "请先禁用设备采集驱动再重新应用模板！");
        return
      }
      this.select_template = row.name; 
      switch(row.protocol) {
        case "Modbus-TCP":
            this.dialogFormTcp = true;
            break;
        case 'Modbus-RTU':
            this.dialogFormRtu = true;
            break;
        case 'Canis Pro采集卡':
            this.dialogFormCanis = true;
            break;
      } 
    },
    clickTable(row,index,e){
        this.$refs.refTable.toggleRowExpansion(row);
      },
    catchange(){
      if(this.form1.typeSelected.length === 0){
        this.$axios.get('apis/device/template', {
          params:{            
                  subdevice: this.subdevice_name
                }
        })
        .then(response => {
          this.tableData = response.data.db;
          this.drive_status = response.data.drive_status
          // console.log(this.tableData)
        })
        .catch(function (error) {
          console.log(error);
        });
      }
      else{
        this.$axios.get('apis/device/template', {
            params:{            
                typeSelected: this.form1.typeSelected
            }
          }).then(response => {
            this.tableData = response.data.db;
            // this.drive_status = response.data.drive_status
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
    getData() {
      this.$axios.get("apis/device/protocol/") //设备协议清单
        .then(response => {
          this.protocolList = response.data.db;
        })
      this.$axios.get('apis/device/template', {
        params:{            
                subdevice: this.subdevice_name
              }
      })
      .then(response => {
        this.tableData = response.data.db;
        this.drive_status = response.data.drive_status

        // console.log(this.tableData)
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    closeDialogTcp(val) {
      this.dialogFormTcp = val;
      this.$emit("dump");
      // this.form1.typeSelected=""
    },
    closeDialogRtu(val) {
      this.dialogFormRtu = val;
      this.$emit("dump");
    },
    closeDialogCanis(val) {
      this.dialogFormCanis = val;
      this.$emit("dump");
    },
    saveTemp(formName){
       var _this = this
       this.$refs[formName].validate((valid) => {
        if (valid) {
          switch(this.templateForm.templatetype) {
          case "modbus":
              _this.dialogFormCreate = false;
              _this.dialogFormCreatedesc = false;
              _this.$axios.post('apis/device/template/create/', {
                code_list: this.dynamicValidateForm.domains,
                template_name: this.templateForm.template_name,
                template_remark: this.templateForm.remark,
                type: "modbus",
                accordname: this.form1.typeSelected
                })
                .then(function (response) {
                  console.log(response.data.message);
                  _this.resetForm(formName);
                  _this.resetForm("dynamicValidateForm");
                })
                .catch(function (error) {
                  console.log(error);
                });
              break;
          case 'canispro':
              _this.dialogFormCreateCanisPro = false;
              _this.dialogFormCreatedesc = false;
              _this.$axios.post('apis/device/template/create/', {
                code_list: this.canisproform.domains,
                template_name: this.templateForm.template_name,
                template_remark: this.templateForm.remark,
                type: "canispro",
                accordname: this.form1.typeSelected
                })
                .then(function (response) {
                  console.log(response.data.message);
                  _this.resetForm(formName);
                  _this.resetForm("canisproform");
                })
                .catch(function (error) {
                  console.log(error);
                });
              break;
          } 
         this.$axios.get('apis/device/template', {
            params:{            
                typeSelected: this.form1.typeSelected
            }
          }).then(response => {
          _this.tableData = response.data.db;
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
    submitForm(formName){
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid){
          this.dialogFormCreatedesc = true;
        }else {
          console.log('error submit!!');
          return false;
        }
      })
     
    },
    submitFormCreate(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            console.log(this.form1.typeSelected[1]);
            switch(this.form1.typeSelected[1]){
              case "Modbus-TCP":
              case 'Modbus-RTU':
                this.dialogFormCreate = true;
                break;
              case 'MQTT':
                this.dialogFormCreateMQTT = true;
              case 'Canis Pro采集卡':
                this.dialogFormCreateCanisPro = true;
            }
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
    resetForm(formName) {
      this.dynamicValidateForm = {
          domains: [{
            function_code: '',
            start_register: '',
            register_num: '',
            property: '',
            format: '',
            rule: {
              sign : "",
              number: ""
            },            
          }],
          template_name: '',
          remark: ""
      };
    },
    removecanisproform(item) {
      var index = this.canisproform.domains.indexOf(item)
      if (this.canisproform.domains.length !== 1) {
        this.canisproform.domains.splice(index, 1)
      }
    },
    removemqttform(item) {
      var index = this.mqttform.domains.indexOf(item)
      if (this.mqttform.domains.length !== 1) {
        this.mqttform.domains.splice(index, 1)
      }
    },
    removeDomain(item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (this.dynamicValidateForm.domains.length !== 1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if(formName === 'mqttform'){
            this.mqttform.domains.push(
               {
                property: "",
                type: "root",
                is_null:'是',
                as_name: ''
              }
            )
          }else if(formName === 'dynamicValidateForm'){
            this.dynamicValidateForm.domains.push({
              function_code: this.dynamicValidateForm.domains[0].function_code,
              start_register: '',
              register_num: '',
              property: '',
              format: '',
              rule: {
                sign : "",
                number: ""
              },                     
            });
          }else if(formName === 'canisproform'){
            this.canisproform.domains.push({
              pip_no: "",
              col: "Sensor2",
              dtype:'',
              round: 'e-6'
            });
          }
        } else {
          console.log('no add!!');
          return false;
        }
      });
        
      }
    }
  
};
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
