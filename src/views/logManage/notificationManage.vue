<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>日志事件</el-breadcrumb-item>
        <el-breadcrumb-item>通知管理</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="row-padding">
          <el-button type="primary" size="small" @click="dialogFormVisible = true">新增</el-button>
          <el-input size="small" placeholder="请输入内容" v-model="searchEvent" class="search-input pull-right">
           <el-button slot="append" icon="el-icon-search" @click="select()"></el-button>
         </el-input>
      </el-row>
      <el-table :data="tableData">
          <el-table-column label="责任人" prop="notice_leader" sortable></el-table-column>
          <el-table-column label="位置" prop="notice_location" sortable></el-table-column>
          <el-table-column label="已通知消息数" prop="notice_message_num" sortable></el-table-column>
          <el-table-column label="最近通知时间" prop="notice_time" sortable></el-table-column>
          <el-table-column label="通知状态">
            <template v-slot="scope">
              <el-switch v-model="scope.row.notice_status" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
           </template>
          </el-table-column>
          <el-table-column label="操作">
            <template v-slot="scope">
              <el-tooltip content="详情" placement="left">
                <el-button icon="el-icon-view" type="text" style="font-size:18px" @click="detail(scope.row)"></el-button>
              </el-tooltip>
              <el-tooltip content="删除" placement="right">
                <el-button icon="el-icon-delete" type="text" style="color: #FF0000;font-size:18px" @click="deleteRow(scope.row)"></el-button>
              </el-tooltip>
            </template>
          </el-table-column>
      </el-table>

      <div class="block row-padding-top" style="float:right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="1"
          :page-sizes="[10,20,30,40,50,60,70,80,90,100]"
          :page-size="10"
          layout="total, sizes, prev, pager, next, jumper"
          :total=count>
        </el-pagination>
      </div>
    <!-- 新增设备弹出框 -->
    <el-dialog title="添加子设备" :visible.sync="dialogFormVisible" custom-class="chile-device-box dialog-form">
      <el-form :model="form" label-position="left" label-width="100px" :rules="rules" ref="form">
        <el-form-item label="责任人:" prop="name">
          <el-input type="text" size="small" v-model="form.name" placeholder="Person liable :case 张三"></el-input>
        </el-form-item>
        <el-form-item label="位置:" prop="location">
          <el-input type="text" size="small" v-model="form.location" placeholder="location :case E5-4F"></el-input>
        </el-form-item>
        <el-form-item label="手机号:" prop="phone">
          <el-input type="text" size="small" v-model="form.phone" placeholder="subdevice position :case 130XXXXXXXX"></el-input>
        </el-form-item>
        <el-form-item label="邮箱:" prop="email" >
          <el-input type="text" size="small" v-model="form.email" placeholder="sbdevice remark :case XXX@XXX.com"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="resetForm('form')">重置</el-button>
        <el-button type="primary" size="small" @click="submitForm('form')">确定</el-button>
      </el-row>
    </el-dialog>
      <el-dialog title="责任人详情" :visible.sync="infoDialog" custom-class="chile-device-box ">
        <el-form :model="inform" label-position="left" label-width="100px" ref="inform">
            <el-form-item label="责任人:">
                <span>{{inform.name}}</span>
            </el-form-item>
            <el-form-item label="手机:">
                <span>{{inform.phone}}</span>
            </el-form-item>
            <el-form-item label="邮箱:">
                <span>{{inform.email}}</span>
            </el-form-item>
            <el-form-item label="位置:">
                <span>{{inform.location}}</span>
            </el-form-item>
        </el-form>
      </el-dialog>
  </el-main>
</template>

<script>
import { checkNull } from '../../until/checkRules'
export default {
  data () {
    // 手机号验证
    var checkPhone = (rule, value, callback) => {
      const phoneReg = /^1[3|4|5|7|8][0-9]{9}$/
      if (!value) {
        return callback(new Error('电话号码不能为空'))
      }
      setTimeout(() => {
        // Number.isInteger是es6验证数字是否为整数的方法,但是我实际用的时候输入的数字总是识别成字符串
        // 所以我就在前面加了一个+实现隐式转换
        if (!Number.isInteger(+value)) {
          callback(new Error('请输入数字值'))
        } else {
          if (phoneReg.test(value)) {
            callback()
          } else {
            callback(new Error('电话号码格式不正确'))
          }
        }
      }, 100)
    }
    // 邮箱验证
    var checkEmail = (rule, value, callback) => {
      // const mailReg = /^([a-zA-Z0-9_-])[email protected]([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      const mailReg = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }
    return {
      searchEvent: '',
      count: 0,
      size: 10,
      page: 1,
      form: { // 表单元素
        name: '',
        location: '',
        messageNum: '0',
        time: '',
        status: '1',
        phone: '',
        email: ''
      },
      inform: {
        name: '',
        phone: '',
        email: '',
        location: ''
      },
      url: '/apis/loginfo/NoticeManager/',
      tableData: [],
      infoDialog: false,
      dialogFormVisible: false,
      rules: { // 表单验证
        name: [
          { required: true, validator: checkNull, trigger: 'blur' }
          // { min: 3, max: 15, message: '长度在 3 到 15 个字符之间', trigger: 'blur' },
          // {validator: duladevicename, trigger: 'blur'}
        ],
        location: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          }
        ],
        phone: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          },
          { validator: checkPhone, trigger: 'blur' }
        ],
        email: [
          {
            required: true, validator: checkNull, trigger: 'blur'
          },
          { validator: checkEmail, trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    this.flush_status()
  },
  methods: {
    flush_status: function () {
      this.$axios.get(this.url + '?size=' + this.size + '&page=' + this.page)
        .then(response => {
          this.tableData = response.data.results
          this.count = response.data.count
        })
    },
    // 启用或者禁用
    chooseStatus (row) {
      var _this = this
      if (row.notice_status === true) {
        this.$axios.get(this.url + '?id=' + row.id + '&status=1')
          .then(function (response) {
            _this.dialogFormVisible = false
            _this.flush_status()
            _this.$Message.SuccessMessage(_this, '启用成功')
          })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        this.$axios.get(this.url + '?id=' + row.id + '&status=0')
          .then(function (response) {
            _this.dialogFormVisible = false
            _this.flush_status()
            _this.$Message.SuccessMessage(_this, '禁用成功')
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    // 获取当前时间并格式化 yyyy-MM-dd hh:mm:ss
    dateFormat () {
      var date = new Date()
      var year = date.getFullYear()
      /* 在日期格式中，月份是从0开始的，因此要加0
          * 使用三元表达式在小于10的前面加0，以达到格式统一  如 09:11:05
          * */
      var month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
      var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
      var hours = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
      var minutes = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
      var seconds = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
      // 拼接
      return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds
    },
    // 重置表单
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    // 提交表单
    submitForm (formName) {
      var _this = this
      var creatTime = this.dateFormat()
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post(this.url, {
            notice_leader: this.form.name,
            notice_location: this.form.location,
            notice_message_num: '0',
            notice_time: creatTime,
            notice_status: 1,
            notice_phone: this.form.phone,
            notice_email: this.form.email
          })
            .then(function (response) {
              _this.dialogFormVisible = false
              _this.resetForm(formName)
              _this.flush_status()
            })
            .catch(function (error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 每页显示的条数改变
    handleSizeChange (val) {
      this.size = val // 改变每页显示的条数
      this.page = 1 // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.flush_status() // 点击每页显示的条数时，显示第一页
      console.log(`每页 ${val} 条`)
    },

    // current-change用于监听页数改变，而内容也发生改变
    handleCurrentChange (val) {
      this.page = val // 改变默认的页数
      this.flush_status() // 切换页码时，要获取每页显示的条数
      console.log(`当前页: ${val}`)
    },
    // 查询
    select () {
      this.$axios.get(this.url)
        .then(response => {
          this.count = response.data.count
          this.$axios.get(this.url + '?size=' + this.count + '&search=' + this.searchEvent)
            .then(response => {
              this.tableData = response.data.results
              this.count = response.data.count
            })
        })
    },
    // 详情
    detail (row) {
      this.inform.name = row.notice_leader
      this.inform.phone = row.notice_phone
      this.inform.email = row.notice_email
      this.inform.location = row.notice_location
      this.infoDialog = true
    },
    // 删除
    deleteRow (row) {
      var _this = this
      this.$confirm('此操作将会删除该条记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        this.$axios.get(_this.url + '?id=' + row.id + '&delete=1')
          .then(function (response) {
            _this.flush_status()
            _this.$message({
              type: 'success',
              message: '删除成功!'
            })
          })
          .catch(function (error) {
            console.log(error)
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
