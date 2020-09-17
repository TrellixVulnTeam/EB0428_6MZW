<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">网关管理</el-breadcrumb-item>
      <el-breadcrumb-item>网关信息</el-breadcrumb-item>
    </el-breadcrumb>
    <div id="info" v-loading= "infoloading">
      <el-row class="row-padding">
        <el-button  type="primary" size="small" icon="el-icon-edit" @click="dialogFormEdit = true" plain>编辑</el-button>
      </el-row>
      <el-row>
       <el-alert title="网关信息为网关扩展信息 Ex:网关与CorePro平台建立连接 网关名称-产品ID-网关秘钥对应为CorePro设备三元组" type="warning" show-icon></el-alert>
      </el-row>
      <el-table :data="tableData"  border>
        <el-table-column label="名称" prop="gateway_name">
          <!-- <template slot-scope="scope">
            <el-tag >{{ scope.row.gatewayname }}</el-tag>
          </template> -->
        </el-table-column>
        <el-table-column label="ID" prop="gateway_key"></el-table-column>
        <el-table-column label="子设备数" prop="gateway_subdevice_num">
          <template slot-scope="scope">
            <el-popover
              ref="popover4"
              placement="right"
              trigger="click">
              <el-table :data="gridData" 
              height="300"
              :show-header="false">
                <el-table-column label="名称" width="120" >
                  <template v-slot="scope">
                    <el-tooltip placement="top">
                      <div slot="content">点击查看详情</div>
                      <el-tag type="text"  @click="getRowInfo(scope.row.subdevice_name)">{{scope.row.subdevice_name}}</el-tag>
                    </el-tooltip>
                  </template>
                </el-table-column>
                <el-table-column sortable min-width="120" label="类型" prop="subdevice_type"></el-table-column>
                <el-table-column sortable min-width="120" label="型号" prop="subdevice_model"></el-table-column>
              </el-table>
            </el-popover>
            <el-tag v-popover:popover4> &nbsp;&nbsp;{{ scope.row.gateway_subdevice_num }}&nbsp;&nbsp; </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="位置信息" prop="gateway_location"></el-table-column>
        <el-table-column label="型号" prop="gateway_model"></el-table-column>
        <el-table-column label="厂商" prop="gateway_trade_name"></el-table-column>
        <el-table-column label="注册信息修改时间" prop="gateway_registration_time"></el-table-column>
        <el-table-column label="描述" prop="gateway_remark"></el-table-column>
      </el-table>
      <el-collapse v-model="activeNames" accordion>
        <el-collapse-item title="历史记录..." name="1">
          <span>三元組</span>
          <el-table
            :data="tableData5"
            :show-header="false"
            style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <span style="color:#3a8ee6" >iotHost、iotPort、iotUsername、iotPassword用於網關與CorePro建立通信</span>
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="iotHost:">
                    <span>{{ props.row.gateway_iothost }}</span>
                  </el-form-item>
                  <el-form-item label="iotPort:">
                    <span>{{ props.row.gateway_iotport }}</span>
                  </el-form-item>
                  <el-form-item label="iotUsername:">
                    <span>{{ props.row.gateway_iotid }}</span>
                  </el-form-item>
                  <el-form-item label="iotPassword:">
                    <span>{{ props.row.gateway_iottoken }}</span>
                  </el-form-item>
                  <el-form-item label="TokenApi:">
                    <el-input width="500px" :value="props.row.gateway_tokenapi" readonly ></el-input>
                  </el-form-item>
                  
                </el-form>
              </template>
            </el-table-column>
            <el-table-column
              label="网关名称"
              min-width="25%"
              prop="gateway_name">
            </el-table-column>
            <el-table-column
              label="网关ID"
              min-width="25%"
              prop="gateway_key">
            </el-table-column>
            <el-table-column
              label="网关秘钥"
              min-width="50%"
              prop="gateway_secret">
            </el-table-column>
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </div>
  <!-- 编辑网关信息弹框 -->
    <el-dialog title="网关扩展信息" :visible.sync="dialogFormEdit" custom-class="chile-device-box dialog-form">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="网关名称:" prop="gateway_name">
          <el-input type="text" size="small" v-model="form.gateway_name" placeholder="Agent name :case Edgebox001"></el-input>
        </el-form-item>
        <el-form-item label="产品ID:" prop="gateway_key">
          <el-input type="text" size="small" v-model="form.gateway_key" placeholder="Agent id :case 6656546464646564"></el-input>
        </el-form-item>
        <el-form-item label="网关秘钥:" prop="gateway_secret">
          <el-input type="text" size="small" v-model="form.gateway_secret" placeholder="Agent sercet :case 654gfgrdsfsf1433rewrw54"></el-input>
        </el-form-item>
        <el-form-item label="tokenApi:" prop="gateway_tokenapi">
          <el-input type="text" size="small" v-model="form.gateway_tokenapi" placeholder="Agent token api :case https://0.0.0.0/auth/api"></el-input>
          <!-- <el-select  size="small" v-model="form.gateway_tokenapi" placeholder="Agent token api :case https://0.0.0.0/auth/api"></el-select> -->

        </el-form-item>
        <el-form-item label="位置信息:" prop="gateway_location">
          <el-input type="text" size="small" v-model="form.gateway_location" placeholder="location :case E5-4F"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="resetForm('form')">重置</el-button>
        <el-button type="primary" size="small" @click="submitForm('form')">确认修改</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
import { checkNull } from '../../until/checkRules';
export default {
  name: "info",
  data() {
    return {
      tableData5: [{
          gatewayname: '<N/A>',
          gatewayid: '<N/A>',
          gatewaysercet: '<N/A>',
          iotHost: '<N/A>',
          iotPort: '<N/A>',
          iotUsername: '<N/A>',
          iotPassword: '<N/A>',
          gatewaytokenapi: '<N/A>'
        }
      ],
      activeNames: [],
      gridData: [],
      dialogFormEdit: false,
      infoloading: true,
      tableData: [
        {
          gateway_name: '<N/A>',
          gateway_id: '<N/A>',
          gateway_sercet: '<N/A>',
          gateway_subdevice_num: '<N/A>',
          gateway_model: '<N/A>',
          gateway_trade_name: '<N/A>',
          gateway_registration_time: '<N/A>',
          gateway_remark: '<N/A>',
          gateway_location: '<N/A>',
        }
      ],
      form: { //表单元素
          gateway_name:'',
          gateway_key:'',
          gateway_secret:'',
          gateway_tokenapi: '',
          gateway_location:''
      },
      rules: { // 表单验证
          gatewayname: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
          gatewayid: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
          gatewaysercet: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ],
          gatewaytokenapi: [
            {
                required: true, validator:checkNull, trigger: "blur"
            }
          ],
          gatewaylocation: [
              {
                required: true, validator: checkNull, trigger: 'blur'
              }
          ]
      },
    };
  },
  methods: {
      submitForm(formName) {
        var _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios.post('apis/agent/info/', {
              params: this.form 
            }).then(response => {
              if(response.data.status_code === 0){
                  this.$Message.SuccessMessage(this, response.data.message);
              }
              else{
                this.$Message.ErrorMessage(this, response.data.error);
              }
              this.dialogFormEdit = false;
              _this.resetForm(formName);
              _this.getData()
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
      resetForm(formName) {
         this.$refs[formName].resetFields();
      },
     getRowInfo(row) {
      window.sessionStorage.setItem('pip_index', JSON.stringify("00"));
      window.sessionStorage.setItem('subdevice', JSON.stringify(row.subdevice_name));
      // window.location.href = "/deviceManage?subdevice="+row.subdevice_name
      // this.$router.push({path: 'deviceManage',query:{subdevice: row.subdevice_name}});
      this.$router.push({path: 'deviceList'});

     },
      getData(){
        this.$axios.get("apis/agent/info/")
        .then(response => {
          this.tableData = response.data.row_data
          this.tableData5 = response.data.history_data

          this.form = response.data.row_data[0]
        
        })  
      }
  },
  // 初始化
  created () {
    this.infoloading = false;
    this.getData()
    this.$axios.get("apis/device/list/")
        .then(response => {
          this.gridData = response.data.db;
        })
  }
};
</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
