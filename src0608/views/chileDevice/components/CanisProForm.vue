<!-- 应用模板弹出框 -->
<template>
    <div class="canisfrom">
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
            <el-form-item label="用户名:" prop="userName">
                <el-input type="text"  style="width:85%" v-model="form.userName" size="small" placeholder="userName"></el-input>
             </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="密码:" prop="pwd">
              <el-input type="text"  style="width:85%" v-model="form.pwd" size="small" placeholder="pwd"></el-input>
             </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span= "12">
            <el-form-item label="采集模式:" prop="mode">
              <el-select size="small"  v-model="form.mode" placeholder="mode">
                <el-option v-for="item in canisform.modeList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="采集频率:" prop="sampleRate" >
              <el-select size="small"  v-model="form.sampleRate" placeholder="sampleRate"
              filterable
              allow-create
              default-first-option
              >
                <el-option v-for="item in canisform.sampleRatelist" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span= "12">
             <el-form-item label="缓冲区大小:" prop="bufferSize">
              <el-select size="small"  v-model="form.bufferSize" placeholder="bufferSize"
              filterable
              allow-create
              default-first-option
              >
                <el-option v-for="item in canisform.bufferSizeList" :key="item.index" :label="item.index" :value="item.index">
                  <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span= "12">
            <el-form-item label="触发方式:" prop="trigger">
              <el-select size="small"  v-model="form.trigger" multiple placeholder="trigger"
                filterable
                allow-create
                default-first-option
               >
                <el-option v-for="item in canisform.triggerList" :key="item.index" :label="item.index" :value="item.index">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span= "12">
             <el-form-item label="绑定驱动:" prop="drive">
              <el-select size="small"  v-model="form.drive" placeholder="请选择要绑定的驱动程序">
                <el-option v-for="item in canisform.driveList" :key="item.index" :label="item.value" :value="item.index">
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
            ip: '192.168.1.96',
            port: '23333',
            userName: "admin",
            pwd: "admin",
            mode: "A",  //采集模式
            bufferSize: "512K",  // 缓存区大小
            sampleRate: "64K",  //采集频率
            trigger: ["IO触发"], 
            drive: ''
            },
        canisform: {
            modeList: [ // 采集模式列表
            ],
            bufferSizeList: [ // 缓存区大小列表         
            ],
            sampleRateList: [ // 采集频率列表 
            ],
            triggerList: [  //触发方式列表

            ],
            driveList: [
            {
                index: 0,
                value: '驱动1'
            }
            ],
          },
        rules: { // 表单验证
          ip: [{required: true, message: 'ip地址不能为空!', trigger:['change', 'blur']}],
          port: [{required: true,message: '请输入端口号!', trigger: ['change', 'blur']}],
          userName:[{required: true, message: '请输入用户名!', trigger: ['change', 'blur']}],
          pwd: [{required: true, message: '请输入密码!', trigger: ['change', 'blur']}],
          mode: [{required: true, message: '请选择采集模式!', trigger: ['change', 'blur']}],
          bufferSize: [{required: true, message: '请选择缓冲区大小!', trigger: ['change', 'blur']}],
          sampleRate: [{required: true, message: '请选择采集频率!', trigger: ['change', 'blur']}],
          trigger: [{required: true, message: '请输入触发模式!', trigger: ['change', 'blur']}],
          drive: [{required: true, message: '请选择驱动名称!', trigger: ['change', 'blur']}],
      },
       }
    },
    created() {
        this.$axios.get("apis/device/canisproform/") //modbus tcp from表单
        .then(response => {
          this.canisform = response.data.db;
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
             type: "canis",
             subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
             template_name: this.templatename,
             content: this.form,
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
    