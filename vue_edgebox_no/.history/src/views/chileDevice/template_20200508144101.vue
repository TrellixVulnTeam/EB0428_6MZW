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
        <el-table-column sortable label="协议名称" prop="protocol">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.protocol === 'Modbus-RTU'" size="medium">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else-if="scope.row.protocol === 'Modbus-TCP'" size="medium" type="success">{{ scope.row.protocol }}</el-tag>
            <el-tag v-else size="medium" type="warning">{{ scope.row.protocol }}</el-tag>

          </template>
        </el-table-column>
        <el-table-column  sortable label="创建时间" prop="createTime"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
        <el-table-column label="操作" width="100">
            <template slot-scope="scope">
                <el-button type="text" size="small" style="color: #08bba2" @click="show(scope.row)">修改</el-button>
                <el-button type="text" size="small" style="color: #FF0000" @click="deleteRow(scope.row.name)">删除</el-button>
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
    <div class="dialogfrommodel">
      <el-dialog   :title="'模板修改('+template_name+')'" :visible.sync="dialogFormCreate"  width= "800px">
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
          <!-- <el-input >321321</el-input> -->
          <el-button type="primary" @click="addDomain('dynamicValidateForm')" size="small" plain>新增属性</el-button>
          <el-button type="primary" @click="updateRow('dynamicValidateForm')" size="small">确认修改</el-button>
        </el-row>
      </el-dialog>
    </div>
  </el-main>
</template>

<script>
export default {
    data() {
        return {
          entdatas:[],  
          entexpands: [],
          tableData: [],
          dialogFormCreate: false,
          template_name: "",
          appforms: {
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
              remark:"",
              rule: {
                sign : "",
                number: ""
              },            
            }],
      },
        }
    },
    created() {
        this.flush_status()
    },
    methods: {

    flush_status() {
        this.$axios.get("apis/device/template") //设备协议清单
        .then(response => {
            this.tableData = response.data.db;
            this.dynamicValidateForm.domains = response.data.info
            console.log(response.data.info)
        })
    },
    show(row){
        this.dialogFormCreate = true;
        this.dynamicValidateForm.domains = row.info2;
        this.template_name = row.name
    },
    //修改模板数据
    updateRow(formName){
      this.$refs[formName].validate((valid) => {
        if (valid) {
            console.log("update")
            var _this = this;
            this.$axios.post('apis/device/template/update/', {
              template_name: _this.template_name,
              code_list: _this.dynamicValidateForm.domains,
          })
          .then(function (response) {
            console.log(response.data.message);
            _this.$Message.SuccessMessage(_this, "修改成功!");
            _this.dialogFormCreate = false;
            _this.flush_status()
          })
          .catch(function (error) {
            console.log(error);
          });
        }else {
          console.log('error submit!!');
          // return false;
        }
      });
    },
      // 删除数据
    deleteRow(rows) {
      this.$Message.WarningAlert(this,'您确定要删除此模板吗？','模板删除').then(
        res => {
          var _this = this;
          this.$axios.post('apis/device/template/delete/', {
            template_name: rows,
          })
          .then(function (response) {
            console.log(response.data.message);
            _this.$Message.SuccessMessage(_this, "删除成功!");
            _this.flush_status()
          })
          .catch(function (error) {
            console.log(error);
          });
          
        }
      );
      
    },
    clickTable(row,index,e){
      this.$refs.refTable.toggleRowExpansion(row);
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
          }
        } else {
          console.log('no add!!');
          return false;
        }
      });
        
      }
    }
    
}

</script>

<style >
.el-col-6 {
  padding: 5px;
}

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