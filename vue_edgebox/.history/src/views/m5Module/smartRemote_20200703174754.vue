<template>
  <el-main class="no-padding smartremote">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>智能产品对接</el-breadcrumb-item>
      <el-breadcrumb-item>智能设备管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-alert title="智能设备扩展模块的远程通信配置" type="success" show-icon></el-alert>
      <el-button type="primary" size="small" @click="newcommuVisible = true"  >新 增</el-button>
      <el-button type="primary" size="small" @click="downorder = true"  >指令下发</el-button>
      <el-input
        placeholder="请输入内容"
        size="small"
        v-model="searchDevice"
        class="pull-right search-input"
      >
        <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
    
    <el-table :data="tableData"  ref="refTable" >
      <el-table-column type="expand">
      <template slot-scope="scope">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="通信设备"><br>
            <el-tag >{{ scope.row.smart_sns.replace(/,/g, "&nbsp;&nbsp;    ")}}</el-tag> 
            <!-- <el-tag  v-for="city in sel_sns" :label="city" :key="city">{{ city}} &nbsp;&nbsp;&nbsp;&nbsp;</el-tag>  -->
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
        <el-table-column label="路径名称" prop="smart_name" min-width="35%"></el-table-column>
        <el-table-column sortable label="活动区域" prop="smart_area" min-width="35%">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.smart_area === 'E5'" size="medium">{{ scope.row.smart_area }}</el-tag>
            <el-tag v-else-if="scope.row.smart_area === 'E6'" size="medium" type="success">{{ scope.row.smart_area }}</el-tag>
            <el-tag v-else size="medium" type="warning">{{ scope.row.smart_area }}</el-tag>

          </template>
        </el-table-column>

        <el-table-column  sortable label="创建时间" prop="create_time" min-width="60%"></el-table-column>
        <el-table-column sortable label="启用状态" min-width="40%">
            <template v-slot="scope">
              <el-switch v-model="scope.row.smart_enable" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
           </template>
        </el-table-column>
        <el-table-column label="描述" prop="smart_remark" min-width="40%"></el-table-column>
        <el-table-column label="操作" width="120">
            <template slot-scope="scope">
                <el-button type="text" size="small" style="color: #08bba2" >修改</el-button>
                <el-button type="text" size="small" style="color: #FF0000" @click="deleteRow(scope.row)">删除</el-button>
            </template>
        </el-table-column>

    </el-table>
    <el-dialog
    
      title="添加一组通信"
      :visible.sync="newcommuVisible"
      width="560px"
      custom-class="smart-box dialog-form"
      :before-close="handleClose">
      <el-form :data="tableData" :rules="rules" ref="form" :model="form" label-position="left" label-width="100px">
        <el-form-item label="通信名称" prop="name">
          <el-input v-model="form.name" size="small"></el-input>
        </el-form-item>
        <el-form-item label="活动区域" prop="region">
          <el-select size="small" v-model="form.region" placeholder="请选择活动区域">
            <el-option label="E5" value="E5"></el-option>
            <el-option label="E6" value="E6"></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="创建时间">
          <el-col :span="11">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
          </el-col>
          <el-col class="line" :span="2">-</el-col>
          <el-col :span="11">
            <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
          </el-col>
        </el-form-item> -->
        <!-- <el-form-item label="即时开启" prop="delivery">
          <el-switch v-model="form.delivery"></el-switch>
        </el-form-item> -->
        <el-form-item label="设备SN" prop="type">
          <!-- <el-checkbox-group v-model="form.type">
            <el-checkbox label="SN001" name="type"></el-checkbox>
            <el-checkbox label="SN002" name="type"></el-checkbox>
            <el-checkbox label="SN003" name="type"></el-checkbox>
          </el-checkbox-group> -->
          <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
            <div style="margin: 15px 0;"></div>
          <el-checkbox-group v-model="form.type" @change="handleCheckedCitiesChange">
            <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <!-- <el-form-item label="其他选项" prop="resource">
          <el-radio-group v-model="form.resource">
            <el-radio label="选项1"></el-radio>
            <el-radio label="选项2"></el-radio>
          </el-radio-group>
        </el-form-item> -->
        <el-form-item label="备注" prop="desc">
          <el-input type="textarea" rows="1" v-model="form.desc"></el-input>
        </el-form-item>

      </el-form>
      <el-row  slot="footer">
        <el-button size="small" type="primary" @click="submitForm('form')">立即创建</el-button>
        <el-button size="small" type="default" @click="resetForm('form')">重置</el-button>
      </el-row>
    </el-dialog>
    <el-dialog
    
      title="对M5设备下发指令"
      :visible.sync="downorder"
      width="560px"
      custom-class="smart-box dialog-form"
      :before-close="handleClose">
      <el-form :data="tableData" :rules="rules" ref="form" :model="form2" label-position="left" label-width="100px">

        <el-form-item label="指令" prop="order">
          <el-input type="textarea" rows="3" v-model="form2.order" placeholder='{"Command":"1","cRed":"off","cYellow":"off","cGreen":"on"}'></el-input>
        </el-form-item>
      <div>{"Command":"1","cRed":"off","cYellow":"off","cGreen":"on"}</div>
      </el-form>
      <el-row  slot="footer">
        <el-button size="small" type="primary" @click="submitForm2('form2')">立即下发</el-button>
        <el-button size="small" type="default" @click="resetForm('form')">重置</el-button>
      </el-row>
    </el-dialog>

  </el-main>
</template>

<script>
let cityOptions = [];

export default {
    data() {
      return {
          checkAll: false,
          checkedCities: [],
          // cityOptions: [],
          cities: [],
          isIndeterminate: true,
          newcommuVisible : false,
          downorder : false,
          is_active : false,
          entdatas:[],  
          entexpands: [],
          tableData: [],
          form: {
            name: '',
            region: '',
            delivery: false,
            type: [],
            resource: '',
            desc: ''
          },
          form2: {

            order: ''
          },
          rules: {
            name: [
              { required: true, message: '请输入名称', trigger: 'blur' },
              { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
            ],
            region: [
              { required: true, message: '请选择活动区域', trigger: 'change' }
            ],
      
            type: [
              { type: 'array', required: true, min: 2, message: '请至少选择两个设备SN', trigger: 'change' }
            ],
            resource: [
              { required: true, message: '请选择活动资源', trigger: 'change' }
            ],
            desc: [
              { required: false, message: '请填写相关备注', trigger: 'blur' }
            ]
          }
      };
    },
    created(){
    // this.getData()
    // // 这是一个定时器
    // this.positionTimer = setInterval(() => {
    //   this.getData()
    // }, 3000)
    this.flush_status()
    },
    destroyed () {
      clearInterval(this.positionTimer)// 清除定时器
      this.positionTimer = null
      // console.log('关闭定时器')
    },
    methods: {
      flush_status: function () {
        this.loading = true,
        this.$axios.get("apis/m5/smartlist/")
          .then(response => {
            this.tableData = response.data.db;
            this.cities = response.data.sns;

          })

        setTimeout(() => {
          this.loading = false;
        }, 300);
      },
      handleClose (done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done()
          })
          .catch(_ => {})
      },
      getData() {
        var _this = this;
        this.$axios.get('/apis/m5/smartlist/')
        .then(response => {
          this.tableData = response.data.db;
          this.cities = response.data.sns;

          // this.loading = false
          _this.flush_status()
        })
        .catch(error => {
          console.log(error)
        })
      },
      // 提交表单
      submitForm(formName) {
        var _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios.post('apis/m5/smartcreate/', {
            smart_name: this.form.name,
            smart_type: this.form.type,
            smart_region: this.form.region,
            smart_remark: this.form.desc
            })
            .then(function (response) {
              console.log(response.data.message);
              _this.newcommuVisible = false
              _this.resetForm(form);
              _this.form.desc= "";
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

            // 提交表单
      submitForm2(formName) {
        var _this = this;

        this.$axios.post('apis/m5/smartorder/', {
        smart_order: this.form2.order
        })
        .then(function (response) {
          console.log(response.data.message);
          
          _this.downorder = false;
          _this.$Message.SuccessMessage(_this, "下发成功!");
          _this.flush_status()
        })
        .catch(function (error) {
          console.log(error);
        });
      },

      // 启用或者禁用
      chooseStatus(row) {
          var _this = this;
          this.$axios.post('apis/m5/smartenable/', {
                smart_name: row.smart_name,
                enable: row.smart_enable
              })
              .then(function (response) {
                _this.$Message.SuccessMessage(_this, response.data.message);
                _this.flush_status()
              })
              .catch(function (error) {
                console.log(error);
              });
      },

      // 删除数据
      deleteRow(rows) {
        var _this = this;
        this.$Message.WarningAlert(this,'您确定要删除此路径吗？','路径删除').then(
          res => {
            // console.log('1111');
            if(rows.smart_enable) {
              this.$Message.WarningAlert(this, "启用状态不能删除！");
            }
            else{
              var _this = this;
              this.$axios.post('apis/m5/smartdelete/', {
                smart_name: rows.smart_name,
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
      resetForm(formName) {
        this.$refs[formName].resetFields();
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
          
      },
      handleCheckAllChange(val) {
        this.form.type = val ? this.cities : [];
        console.log(this.form.type);
        console.log("aaaaaa");
        this.isIndeterminate = false;
      },
      handleCheckedCitiesChange(value) {
        let checkedCount = value.length;
        console.log(checkedCount);
        console.log(this.cities.length);
        
        this.checkAll = checkedCount === this.cities.length;
        console.log(this.checkAll);
        this.isIndeterminate = false;
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
.serch_input {
    width: 25%;
    float: right;

}
</style>