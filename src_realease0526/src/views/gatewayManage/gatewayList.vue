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
      <el-table :data="tableData"  border>
        <el-table-column label="名称" prop="gatewayname"></el-table-column>
        <el-table-column label="ID" prop="gatewayid"></el-table-column>
        <el-table-column label="子设备数" prop="childDevices"></el-table-column>
        <el-table-column label="位置信息" prop="gatewaylocation"></el-table-column>
        <el-table-column label="型号" prop="factoryModel"></el-table-column>
        <el-table-column label="厂商" prop="factoryName"></el-table-column>
        <el-table-column label="注册信息修改时间" prop="registrationTime"></el-table-column>
        <el-table-column label="描述" prop="description"></el-table-column>
      </el-table>
      <el-row class="row-padding">
        <echarts ref="echarts"></echarts>
      </el-row>
    </div>
  <!-- 编辑网关信息弹框 -->
    <el-dialog title="网关注册" :visible.sync="dialogFormEdit" custom-class="chile-device-box dialog-form">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="网关名称:" prop="gatewayname">
          <el-input type="text" size="small" v-model="form.gatewayname" placeholder="Agent name :case Edgebox001"></el-input>
        </el-form-item>
        <el-form-item label="产品ID:" prop="gatewayid">
          <el-input type="text" size="small" v-model="form.gatewayid" placeholder="Agent id :case 6656546464646564"></el-input>
        </el-form-item>
        <el-form-item label="网关秘钥:" prop="gatewaysercet">
          <el-input type="text" size="small" v-model="form.gatewaysercet" placeholder="Agent sercet :case 654gfgrdsfsf1433rewrw54"></el-input>
        </el-form-item>
        <el-form-item label="tokenApi:" prop="gatewaytokenapi">
          <el-input type="text" size="small" v-model="form.gatewaytokenapi" placeholder="Agent token api :case https://0.0.0.0/auth/api"></el-input>
        </el-form-item>
        <el-form-item label="位置信息:" prop="gatewaylocation">
          <el-input type="text" size="small" v-model="form.gatewaylocation" placeholder="location :case E5-4F"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small">重置</el-button>
        <el-button type="primary" size="small">确定</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
import { checkNull } from '../../until/checkRules'
import echarts from './components/echarts.vue'
export default {
  name: 'info',
  data () {
    return {
      dialogFormEdit: false,
      infoloading: true,
      tableData: [
        {
          gatewayname: '<N/A>',
          gatewayid: '<N/A>',
          gatewaysercet: '<N/A>',
          childDevices: '<N/A>',
          factoryModel: '<N/A>',
          factoryName: '<N/A>',
          registrationTime: '<N/A>',
          description: '<N/A>',
          gatewaylocation: '<N/A>'
        }
      ],
      form: { // 表单元素
        gatewayname: '',
        gatewayid: '',
        gatewaysercet: '',
        gatewaytokenapi: '',
        gatewaylocation: ''
      },
      rules: { // 表单验证
        gatewayname: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        gatewayid: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        gatewaysercet: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        gatewaytokenapi: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        gatewaylocation: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ]
      }
    }
  },
  methods: {
  },
  components:{
    echarts
  },
  // 初始化
  created () {
    this.infoloading = false
    this.$axios.get('apis/agent/info/')
      .then(response => {
        this.tableData[0].gatewayname = response.data.gateway_name
        this.tableData[0].gatewayid = response.data.gateway_key
        this.tableData[0].gatewaysercet = response.data.gateway_sercet
        this.tableData[0].childDevices = response.data.gateway_subdevice_num
        this.tableData[0].factoryModel = response.data.gateway_model
        this.tableData[0].factoryName = response.data.gateway_trade_name
        this.tableData[0].registrationTime = response.data.gateway_registration_time
        this.tableData[0].description = response.data.gateway_remark
        this.tableData[0].gatewaylocation = response.data.gateway_location
      })
  },
  mounted(){
    this.$refs["echarts"].bar()
    this.$refs["echarts"].line()
    this.$refs["echarts"].pie()
  }
}
</script>

<style scoped>
</style>
