<template>
  <el-main class="no-padding">
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>用户中心</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-small-padding">
      <el-alert title="用户中心可查看用户信息及对用户的管理！" type="info" show-icon></el-alert>
    </el-row>
    <!-- 操作 -->
    <el-row class="row-padding">
      <!-- <el-button size="small" :disabled="enableBtn" plain>批量启用</el-button>
      <el-button size="small" :disabled="unableBtn" plain>批量禁用</el-button>
      <el-button size="small" :disabled="deleteBtn" plain>批量删除</el-button> -->
      <el-button type="primary" size="small" @click="addUser" :disabled="!isuser">新增用户</el-button>
      <el-button type="success" size="small" @click="flush_status" plain >刷 新</el-button>

      <el-input
        placeholder="请输入内容"
        size="small"
        v-model="searchUser"
        class="pull-right search-input"
      >
        <el-button type="primary" slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </el-row>
    <el-table :data="userInformation" v-loading="loading" :row-class-name="changeClassName">
      <el-table-column min-width="50" label="用户名" prop="username" align="center" sortable>
        <template slot-scope="scope">
          <!-- <span v-show="!scope.row.isShow&&!scope.row.is_staff"><el-tag type="info">{{scope.row.username}}</el-tag></span> -->
          <!--如果不是管理员-->
          <span v-if="(!scope.row.isShow || (!scope.row.is_Edit && scope.row.exis)) && !scope.row.is_superuser"><el-tag type="success">{{scope.row.username}}</el-tag></span>
          <!--如果是管理员-->
          <span v-if="(!scope.row.isShow || !scope.row.is_Edit) && scope.row.is_superuser"><el-tag>{{scope.row.username}}</el-tag></span>
          <el-input class="edit" size="small" v-model="scope.row.username" v-if="scope.row.isShow && !scope.row.isEdit"></el-input>
        </template>
      </el-table-column>
      <el-table-column min-width="70" label="手机号" prop="phone_number" align="center" sortable>
        <template slot-scope="scope">
          <span v-if="!scope.row.isShow">{{scope.row.phone_number}}</span>
          <el-input class="edit" size="small" v-model="scope.row.phone_number" v-if="scope.row.isShow" maxlength="11"></el-input>
        </template>
      </el-table-column>
      <el-table-column min-width="120" label="邮箱" prop="email" align="center" sortable>
        <template slot-scope="scope">
          <span v-if="!scope.row.isShow">{{scope.row.email}}</span>
          <el-input class="edit" size="small" v-model="scope.row.email" v-if="scope.row.isShow"></el-input>
        </template>
      </el-table-column>
      <el-table-column min-width="65" label="身份证后六位" prop="user_id_six" align="center" sortable>
        <template slot-scope="scope">
          <span v-if="!scope.row.isShow">{{scope.row.user_id_six}}</span>
          <el-input class="edit" size="small" v-model="scope.row.user_id_six" v-if="scope.row.isShow" maxlength="6"></el-input>
        </template>
      </el-table-column>
      <el-table-column min-width="120" label="上次登陆时间" align="center" sortable>
        <template slot-scope="scope">
          <span v-show="!scope.row.isShow">{{scope.row.last_login}}</span>
          <span v-show="scope.row.isShow">/</span>
        </template>
      </el-table-column>
      <!-- <el-table-column min-width="50" label="是否激活" align="center" sortable>
        <template slot-scope="scope">
          <span v-show="!scope.row.isShow">{{scope.row.is_active}}</span>
          <span v-show="scope.row.isShow">/</span>
        </template>
      </el-table-column> -->
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-button type="text"  @click="edit(scope.row)" v-if="!scope.row.isShow" :disabled="!isuser">编辑</el-button>
          <el-button type="text" class="button-red" @click="deleteRow(scope.row)" v-if="!scope.row.isShow" :disabled="!isuser">删除</el-button>
          <el-button type="text" class="button-green" @click="save(scope.row)" v-if="scope.row.isShow" :disabled="!isuser">保存</el-button>
          <el-button type="text" class="button-grey" @click="close(scope.row)" v-if="scope.row.isShow">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-main>
</template>

<script>
export default {
  data () {
    return {
      loading: true,
      searchUser: '',
      userInformation: []
    }
  },
  created () {
    if (JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['isUser'] == true) this.isuser = true
    this.getUserList()
    this.loading = false
    // this.userInformation.userName = JSON.parse(localStorage.getItem("tokenLogin"))["name"]
  },
  methods: {
    getUserList () {
      var _this = this
      this.$axios.get('apis/user/user_info/' + JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['name'])
        .then(response => {
          if (response.data.error_code == 0) {
            _this.userInformation = response.data.error_msg
            for (var i = 0; i < _this.userInformation.length; i++) {
              // if(!_this.userInformation[i].hasOwnProperty("isShow")){
              // }
              _this.userInformation[i]['isShow'] = false
              _this.userInformation[i]['isEdit'] = false
              _this.userInformation[i]['exis'] = true
            }
          } else if (response.data.error_code == 1) {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
          } else {
            _this.$Message.ErrorMessage(_this, '未知错误')
          }
        })
    },
    // 删除数据
    deleteRow (row) {
      if (JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['isUser'] == false) return this.$Message.WarningMessage(this, '该功能暂未开放！')
      var isDele = false
      this.userInformation.forEach((v, i) => {
        if (v.isShow === true) isDele = true
      })
      if (isDele === true) return this.$Message.ErrorMessage(this, '有一个用户信息正在编辑，请先确认是否编辑完成！')
      if (row.username == JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['name']) return this.$Message.WarningMessage(this, '暂不支持删除当前用户！')
      var _this = this
      this.$Message.WarningAlert(this, '您确定要删除此用户吗？', '用户删除').then(
        res => {
          this.$axios.post('apis/user/delete_user', {
            username: JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['name'],
            delete_user: row.username,
            super_password: 'admin'
          }).then(response => {
            if (response.data.error_code == 0) {
              _this.$Message.SuccessMessage(_this, response.data.error_msg)
              _this.getUserList()
            } else if (response.data.error_code == 1) {
              _this.$Message.ErrorMessage(_this, response.data.error_msg)
            } else {
              _this.$Message.ErrorMessage(_this, response.data.error_msg)
            }
          })
          // _this.userInformation.forEach((v, i) => {
          //   if (row.userName === v.userName) {
          //     // i 为选中的索引
          //     _this.userInformation.splice(i, 1)
          //   }
          // })
        }
      )
    },
    flush_status: function () {
      this.loading = true,
      this.getUserList()
      setTimeout(() => {
        this.loading = false
      }, 300)
    },
    addUser () {
      if (JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['isUser'] == false) return this.$Message.WarningMessage(this, '该功能暂未开放！')
      if (this.userInformation[0].isShow === true) return this.$Message.ErrorMessage(this, '有一个新建用户暂未确认，请先确认新建用户是否创建！')
      // throw SyntaxError("有一个新建用户暂未确认，请先确认新建用户是否创建！");
      this.userInformation.unshift({
        userName: '',
        telephone: '',
        mail: '',
        IDCard: '',
        exis: false,
        isShow: true,
        isEdit: false
      })
      setTimeout(function () {
        $('.el-table__row').eq(0).css('background', 'yellow')
        $('input').eq(1).focus()
      }, 100)
      setTimeout(function () {
        $('.el-table__row').eq(0).css('background', '')
      }, 1000)
    },
    edit (row) {
      var isEdit = false
      this.userInformation.forEach((v, i) => {
        if (v.isShow === true) isEdit = true
      })
      if (isEdit === true) return this.$Message.ErrorMessage(this, '有一个用户信息正在编辑，请先确认是否编辑完成！')
      // if(JSON.parse(localStorage.getItem("tokenLogin"))["isUser"] == false) return this.$Message.WarningMessage(this, "该功能暂未开放！")
      row.isShow = true
      row.isEdit = true
      // var item = list[index];
      // item.show = false;
      this.$set(this.userInformation, row.index, row)
    },
    save (row) {
      var _this = this
      console.log(row.user_id_six)

      if (JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['isUser'] == false) return this.$Message.WarningMessage(this, '该功能暂未开放！')
      if (row.username == '' || row.username == null) return this.$Message.ErrorMessage(this, '用户名不能为空!')
      if (!(/^[a-zA-Z0-9]/).test(row.username)) return this.$Message.ErrorMessage(this, '用户名不能包含特殊字符!')
      if (row.phone_number == '' || row.phone_number == null) return this.$Message.ErrorMessage(this, '手机号不能为空!')
      if (!(/^1[3456789]\d{9}$/.test(row.phone_number))) return this.$Message.ErrorMessage(this, '手机号格式不正确!')
      if (row.email == '') return this.$Message.ErrorMessage(this, '邮箱不能为空!')
      if (!(/^([a-zA-Z]|[0-9])(\w|\-|\.)+@(\S)+\.([a-zA-Z]{2,4})$/.test(row.email))) return this.$Message.ErrorMessage(this, '邮箱格式不正确!')
      if (row.user_id_six == '' || row.user_id_six == null) return this.$Message.ErrorMessage(this, '身份证后六位不能为空!')
      if (!(/[0-9]+[0-9xX]$/.test(row.user_id_six))) return this.$Message.ErrorMessage(this, '身份证后六位格式不正确!')
      if (row.user_id_six.length < 6) return this.$Message.ErrorMessage(this, '请输入身份证后六位!')

      if (row.exis == true) {
        this.$axios.post('apis/user/user_info', {
          username: row.username,
          user_id_six: row.user_id_six,
          phone_number: row.phone_number,
          email: row.email
        }).then(response => {
          if (response.data.error_code == 0) {
            _this.$Message.SuccessMessage(_this, response.data.error_msg)
            _this.getUserList()
          } else if (response.data.error_code == 1) {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
          } else {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
          }
        })
      } else if (row.exis == false) {
        this.$axios.post('apis/user/create_user', {
          username: JSON.parse(this.$secre.changeSecret(localStorage.getItem('tokenLogin')))['name'],
          new_user: row.username,
          user_id_six: row.user_id_six,
          phone_number: row.phone_number,
          email: row.email,
          password: 'admin'
        }).then(response => {
          if (response.data.error_code == 0) {
            _this.$Message.SuccessMessage(_this, response.data.error_msg)
            // _this.userInformation[0].isShow = false
            _this.getUserList()
          } else if (response.data.error_code == 1) {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
          } else {
            _this.$Message.ErrorMessage(_this, response.data.error_msg)
          }
        })
      }
    },
    close (row) {
      if (row.exis == true) {
        row.isShow = false
        this.$set(this.userInformation, row.index, row)
      } else if (row.exis == false) {
        this.userInformation.splice(row.index, 1)
      }
    },
    changeClassName ({ row, rowIndex }) {
      row.index = rowIndex
      if (row.is_superuser == true) {
        return 'is_manage'
      } else if (row.is_superuser == false) {
        return 'is_user'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0;
}
.el-table .el-input{
  width: 100%;
}
.el-input--small .el-input__inner{
  text-align: center;
}
.button-red{
  color: #FF0000;
}
.button-green{
  color: #67c23a;
}
.button-grey{
  color: #909399;
}
.el-table >>> .is_manage{
  border: 1px solid black;
  background-color: #ecf5ff;
}
.el-table >>> .is_user{
  border: 1px solid black;
  background-color: #f0f9eb
}
.el-table >>> td{
  border-bottom: 2px solid #EBEEF5;
}
</style>
