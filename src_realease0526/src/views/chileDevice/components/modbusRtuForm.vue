<!-- 应用模板弹出框 -->
<template>
    <div>
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-row>
          <el-col :span="12">
            <el-form-item label="串口号:" prop="serial">
              <el-select size="small"  v-model="form.serial" placeholder="COM口选择">
                <el-option v-for="item in modbusrtuform.serialList" :disabled="item.disabled" :key="item.index" :label="item.index" :value="item.index">
                 <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
             </el-form-item>
          </el-col>
          <el-col :span="12" >
            <el-form-item label="波特率:" prop="baudRate">
              <el-select size="small" v-model="form.baudRate" placeholder="波特率选择">
                <el-option v-for="item in modbusrtuform.baudRateList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="数据位:" prop="dataBit">
              <el-select size="small" v-model="form.dataBit" placeholder="数据位选择">
                <el-option v-for="item in modbusrtuform.bitList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
             </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="奇偶校验:" prop="parity">
              <el-select size="small" v-model="form.parity" placeholder="校验选择">
                <el-option v-for="item in modbusrtuform.parityList" :key="item.index" :label="item.index" :value="item.index">

                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="停止位:" prop="stopBit">
              <el-select size="small"  v-model="form.stopBit" placeholder="停止位选择">
                <el-option v-for="item in modbusrtuform.stopBitList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="回复超时:" prop="timeout">
              <el-select size="small"  v-model="form.timeout" placeholder="回复超时设置">
                <el-option v-for="item in modbusrtuform.timeoutList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="从站地址:" prop="address">
               <el-select size="small"  v-model="form.address" placeholder="Slave地址"
                filterable
                allow-create
                default-first-option
               >
                <el-option v-for="item in modbusrtuform.addressList" :key="item.index" :label="item.index" :value="item.index">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="读写周期:" prop="cycle" >
              <el-select size="small"  v-model="form.cycle" placeholder="读写周期设置"
              filterable
              allow-create
              default-first-option
              >
                <el-option v-for="item in modbusrtuform.cycleList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="绑定驱动" prop="drive">
          <el-select size="small"  v-model="form.drive" placeholder="请选择要绑定的驱动程序">
            <el-option v-for="item in modbusrtuform.driveList" :key="item.index" :label="item.index" :value="item.index">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <el-row  slot="footer">
        <el-button type="primary" size="small" @click="applyForm('form')">应用</el-button>
        <el-button type="default" size="small" @click="resetForm('form')">重置</el-button>
        <!-- <el-button type="default" size="small" @click="close">重置</el-button> -->

      </el-row>
    </div>
</template>

<script>
export default {
  props: ['templatename'],
  data () {
    return {
      subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
      form: {
        serial: 'COM1',
        dataBit: '8',
        baudRate: '9600',
        parity: 'None,无校验',
        stopBit: '1',
        timeout: '0.5',
        cycle: '3.0',
        address: '',
        drive: ''
      },
      modbusrtuform: {
        serialList: [ // 串口号列表
        ],
        bitList: [ // 数据位列表
        ],
        baudRateList: [ // 波特率列表
        ],
        parityList: [ // 奇偶校验列表
        ],
        stopBitList: [ // 停止位列表
        ],
        timeoutList: [ // 回复超时列表
        ],
        cycleList: [ // 读写周期列表
        ],
        addressList: [ // slave地址
        ],
        driveList: []
      },
      rules: { // 表单验证
        serial: [{ required: true, message: '请选择设备COM口!', trigger: ['change', 'blur'] }],
        databit: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        baudRate: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        parity: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        stopBit: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        timeout: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        cycle: [{ required: true, message: '请选择!', trigger: ['change', 'blur'] }],
        address: [{ required: true, message: '请选择slave从机地址!', trigger: ['change', 'blur'] }],
        drive: [{ required: true, message: '请选择驱动名称!', trigger: ['change', 'blur'] }]
      }
    }
  },
  created () {
    this.$axios.get('apis/device/modbusrtuform/') // modbus rtu from表单
      .then(response => {
        this.modbusrtuform = response.data.db
      })
  },
  methods: {
    // 重置表单
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    close () {
      this.$emit('CloseDialog', false)
    },
    applyForm (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/template/apply/', {
            type: 'rtu',
            subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
            template_name: this.templatename,
            serial: this.form.serial,
            databit: this.form.dataBit,
            baudRate: this.form.baudRate,
            parity: this.form.parity,
            stopBit: this.form.stopBit,
            timeout: this.form.timeout,
            cycle: this.form.cycle,
            address: this.form.address,
            drive: this.form.drive
          })
            .then(function (response) {
              console.log(response.data.message)
              _this.resetForm(formName)
              _this.$Message.SuccessMessage(_this, response.data.message)
              _this.close()
            })
            .catch(function (error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
/* .dialog-form .el-dialog__body {
    padding: 10px 20px 15px 20px;
} */
</style>
