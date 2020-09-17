<template>
    <div>
      <el-form label-position="top" :model="form" ref="form" :rules="rules">
        <el-form-item prop="device_type">
          <h1>设备类型: {{device_type}}</h1>
        </el-form-item>
        <el-form-item prop="data_type">
          <h1>数据类型: </h1>
          <el-select size="small" v-model="form.data_type" placeholder="请选择数据类型">
            <el-option v-for="(item, key) in smtform.data_types" :key="item" :label="key" :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="file_type">
          <h1>文件类型: {{file_type}}</h1>
        </el-form-item>
        <el-card v-if="form.data_type==='local files'||form.data_type==='shared files'">
          <el-form-item v-if="form.data_type==='shared files'" prop="host">
            共享主机IP:
            <el-input v-model="form.host" placeholder="请输入共享主机IP" value="smtform.host"></el-input>
          </el-form-item>
          <el-form-item prop="src_file_folder">
            文件路径：
            <el-input v-model="form.src_file_folder" placeholder="请输入源文件路径" value="smtform.src_file_folder"></el-input>
            <!-- <el-input type="button" @click="dataTypeOnChange()" value="提交"></el-input> -->
          </el-form-item>
          <el-form-item prop="file_name_regular">
            正则表达式:
            <el-input v-model="form.file_name_regular" placeholder="请输入正则表达式" value="smtform.file_name_regular"></el-input>
            <!-- <el-input type="button" @click="dataTypeOnChange()" value="提交"></el-input> -->
          </el-form-item>
          <el-form-item prop="cycle_time">
            采集周期：
            <el-input type="number" v-model="form.cycle_time" placeholder="请输入采集周期" value="smtform.cycle_time"></el-input>
            <!-- <el-input type="button" @click="dataTypeOnChange()" value="提交"></el-input> -->
          </el-form-item>
        </el-card>
        <el-card v-if="form.data_type==='database'">
          数据库类型:
          <el-form-item prop="db_type">
            <el-select size="small" v-model="form.db_type" placeholder="请选择数据库类型" >
              <el-option v-for="item in smtform.db_types" :key="item" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          数据库主机IP:
          <el-form-item prop="host">
            <el-input v-model="form.host" placeholder="请输入数据库主机IP"></el-input>
          </el-form-item>
          数据库端口:
          <el-form-item prop="port">
            <el-input v-model="form.port" placeholder="请输入数据库主机端口"></el-input>
          </el-form-item>
          用户名:
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="请输入数据库用户名"></el-input>
          </el-form-item>
          密码:
          <el-form-item prop="password">
            <el-input type="password" v-model="form.password" placeholder="请输入数据库密码"></el-input>
          </el-form-item>
          数据库名:
          <el-form-item prop="db_name">
            <el-input v-model="form.db_name" placeholder="请输入数据库名"></el-input>
          </el-form-item>
          SQL查询语句:
          <el-form-item prop="sql">
            <el-input v-model="form.sql" placeholder="请输入数据库查询语句"></el-input>
          </el-form-item>
          <el-form-item prop="cycle_time">
            采集周期：
            <el-input type="number" v-model="form.cycle_time" placeholder="请输入采集周期" value="smtform.cycle_time"></el-input>
            <!-- <el-input type="button" @click="dataTypeOnChange()" value="提交"></el-input> -->
          </el-form-item>
        </el-card>
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
  props: ['template_name', 'device_type', 'file_type', 'category', 'flushTemplate'],
  data () {
    return {
      sub_device_name: JSON.parse(sessionStorage.getItem('sub_device_name')),
      form: {
        device_type: this.device_type,
        data_type: 'local files',
        file_type: this.file_type,
        src_file_folder: 'E:\\Desktop\\SMT Test',
        file_name_regular: '.*\\.csv$',
        cycle_time: 3,
        db_type: 'MsSQL',
        host: 'F1332942-TSBG\\SQLEXPRESS',
        port: 1433,
        username: 'F1332942-TSBG\\Jackie',
        password: 'Foxconn6312',
        sql: "select a.cModel,a.BoardSN,a.TopBtm,a.CompName,a.idStation,a.errType,a.realErr,CONVERT(varchar(100),a.Modify_Date, 20) 'md',a.Modifier,a.algorithm,CONVERT(varchar(100),a.fdate, 20) 'fd',b.BkErrName 'err1' from FovWin a left join Error b on a.errType=b.errType left join Error c on a.realErr=c.errType where  a.Modify_Date>='%s' order by a.Modify_Date asc",
        db_name: 'AOI2'
      },
      smtform: {
        data_types: { // 数据类型
        },
        src_file_folder: '', // 源文件路径
        file_name_regular: '', // 文件正则表达式
        cycle_time: 3, // 循环采集周期
        db_types: [ // 数据库类型
        ],
        host: '', // 主机ip
        port: 1433,
        username: 'F1332942-TSBG\\Jackie',
        password: 'Foxconn6312',
        sql: "select a.cModel,a.BoardSN,a.TopBtm,a.CompName,a.idStation,a.errType,a.realErr,CONVERT(varchar(100),a.Modify_Date, 20) 'md',a.Modifier,a.algorithm,CONVERT(varchar(100),a.fdate, 20) 'fd',b.BkErrName 'err1' from FovWin a left join Error b on a.errType=b.errType left join Error c on a.realErr=c.errType where  a.Modify_Date>='%s' order by a.Modify_Date asc",
        db_name: 'AOI2'
      },
      rules: { // 表单验证
        data_type: [{ required: true, message: '请选择数据类型!', trigger: ['change', 'blur'] }],
        file_type: [{ required: true, message: '请选择文件类型!', trigger: ['change', 'blur'] }],
        src_file_folder: [{ required: true, message: '请输入源文件路径!', trigger: ['change', 'blur'] }],
        file_name_regular: [{ required: true, message: '请输入源文件正则表达式!', trigger: ['change', 'blur'] }],
        cycle_time: [{ required: true, message: '请输入采集周期!', trigger: ['change', 'blur'] }],
        db_type: [{ required: true, message: '请输入数据库类型!', trigger: ['change', 'blur'] }],
        host: [{ required: true, message: '请输入主机IP!', trigger: ['change', 'blur'] }],
        port: [{ required: true, message: '请输入主机端口!', trigger: ['change', 'blur'] }],
        username: [{ required: true, message: '请输入用户名!', trigger: ['change', 'blur'] }],
        password: [{ required: true, message: '请输入密码!', trigger: ['change', 'blur'] }],
        sql: [{ required: true, message: '请输入sql查询语句!', trigger: ['change', 'blur'] }],
        db_name: [{ required: true, message: '请输入数据库名!', trigger: ['change', 'blur'] }]
      }
    }
  },
  created () {
    this.$axios.get('apis/device/smtform/') // smt from表单
      .then(response => {
        this.smtform = response.data.db
        console.log(JSON.stringify(this.smtform))
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
      console.log(formName)
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/applyTemplate', {
            sub_device_name: this.sub_device_name,
            template_name: this.template_name,
            category: this.category,
            collect_config: this.form
          })
            .then(response => {
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
        setTimeout(() => {
          this.flushTemplate()
        }, 300)
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
