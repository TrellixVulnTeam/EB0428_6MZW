<!-- 应用模板弹出框 -->
<template>
    <div class="tcpfrom">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-row>
          <el-col :span= "12">
            <el-form-item label="IP地址:" prop="ip">
                <el-input type="text"  style="width:85%" v-model="form.ip" size="small" placeholder="IP address"></el-input>
             </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="端口号:" prop="port">
              <el-input type="text"  style="width:85%" v-model="form.port" size="small" placeholder="IP port"></el-input>
             </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          
          <el-col :span= "12">
            <el-form-item label="回复超时:" prop="timeout">
              <el-select size="small"  v-model="form.timeout" placeholder="回复超时设置">
                <el-option v-for="item in modbustcpform.timeoutList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="读写周期:" prop="cycle" >
              <el-select size="small"  v-model="form.cycle" placeholder="读写周期设置"
              filterable
              allow-create
              default-first-option
              >
                <el-option v-for="item in modbustcpform.cycleList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span= "12">
             <el-form-item label="绑定驱动:" prop="drive">
              <el-select size="small"  v-model="form.drive" placeholder="请选择要绑定的驱动程序">
                <el-option v-for="item in modbustcpform.driveList" :key="item.index" :label="item.value" :value="item.index">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="从站地址:" prop="address">
              <el-select size="small"  v-model="form.address" multiple placeholder="Slave地址"
                filterable
                allow-create
                default-first-option
               >
                <el-option v-for="item in modbustcpform.addressList" :key="item.index" :label="item.value" :value="item.index">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          
        </el-row>
       
        
      </el-form>
      <el-row  slot="footer">
        <el-button type="primary" size="small" @click="applyForm('form')">应用</el-button>
        <el-button type="default" size="small" @click="resetForm('form')">重置</el-button>
      </el-row>
    </div>
</template>


<script>
export default {
    props: ['templatename'],

    data() {
       return {
        form: {
            ip: '10.18.157.43',
            port: '502',
            address: [],
            timeout: '0.5',
            cycle: '3.0',
            drive: ''
            },
        modbustcpform: {
            timeoutList: [ // 回复超时列表
            ],
            cycleList: [ // 读写周期列表         
            ],
            addressList: [ // slave地址
            ],
            driveList: [
            {
                index: 0,
                value: '驱动1'
            },
            {
                index: 1,
                value: '驱动2'
            },
            {
                index: 2,
                value: '驱动3'
            },
            {
                index: 3,
                value: '驱动4'
            }
            ],
          },
        rules: { // 表单验证
          ip: [{required: true, message: 'ip地址不能为空!', trigger:['change', 'blur']}],
          port: [{required: true,message: '请输入端口号!', trigger: ['change', 'blur']}],
          address:[{required: true, message: '请选择slave从机地址!', trigger: ['change', 'blur']}],
          timeout: [{required: true, message: '请选择!', trigger: ['change', 'blur']}],
          cycle: [{required: true, message: '请选择!', trigger: ['change', 'blur']}],
          drive: [{required: true, message: '请选择驱动名称!', trigger: ['change', 'blur']}],
      },
       }
    },
    created() {
        this.$axios.get("apis/device/modbustcpform/") //modbus tcp from表单
        .then(response => {
        this.modbustcpform = response.data.db;
        })
    },
    methods: {
      // 重置表单
      resetForm(formName) {
          this.$refs[formName].resetFields();
      },
      close() {
        this.$emit("CloseDialog", false)
      },
      applyForm(formName) {
        var _this = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$axios.post('apis/device/template/apply/', {
             type: "tcp",
             subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
             template_name: this.templatename,
             ip: this.form.ip,
             port: this.form.port,
             timeout: this.form.timeout,
             cycle: this.form.cycle,
             address: this.form.address,
             drive: this.form.drive,
            })
            .then(function (response) {
              console.log(response.data.message);
              _this.resetForm(formName);
              _this.$Message.SuccessMessage(_this, response.data.message);
              _this.close()
            })
            .catch(function (error) {
              console.log(error);
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
}
</script>

<style scoped>
  </style>
    