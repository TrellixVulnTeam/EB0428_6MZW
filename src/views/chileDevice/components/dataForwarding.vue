<template>
  <el-main class="no-padding">
    <el-alert
      title="提示: 每个设备最多可配置四条转发路径;批量操作时请先关闭自动刷新"
      type="warning"
      show-icon>
    </el-alert>
    <div
      v-loading="loading"
     >
    <el-row class="row-padding row" >
      <el-button size="small" :disabled="enableBtn" plain @click="batchEnable(true)">批量启用</el-button>
      <el-button size="small" :disabled="disabledBtn" plain @click="batchEnable(false)">批量禁用</el-button>
      <el-button size="small" :disabled="deleteBtn" plain @click="bulkDelete()">批量删除</el-button>
      <el-tooltip content="点击新增路径">
        <el-button type="primary" size="small" @click="dialogFormVisible = true">新增</el-button>
      </el-tooltip>
      <el-tooltip content="点击刷新路径">
        <el-button type="success" size="small" @click="flush_status(false)" icon="el-icon-refresh" plain>刷新</el-button>
      </el-tooltip>
      &nbsp;&nbsp;&nbsp;&nbsp;
      <span  v-if="dataFreshinterval === null">
        <el-tooltip content="点击开启自动刷新">
          <el-button type="success" size="small" @click="startFresh()" icon="el-icon-refresh" plain>自动刷新</el-button>
        </el-tooltip>
      </span>
      <span v-else>
        <el-tooltip content="点击关闭自动刷新">
          <el-button type="primary" size="small" @click="closeFresh()">关闭自动刷新</el-button>
        </el-tooltip>
      </span>
      <span style="width: 500px"><h1 style="padding-right: 10px; color:#ff002fb3">采集驱动状态消息: {{ drive_status_msg }}</h1></span>
    </el-row>
    <el-table
    :data="pathListTable"
    :row-class-name="tableRowIndexArray"
    @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" min-width="2%" aria-disabled=""></el-table-column>
      <!-- <el-table-column label="序号" prop="index"></el-table-column> -->
      <el-table-column min-width="15%" label="路径名称" prop="path_name"></el-table-column>
      <el-table-column min-width="15%" label="类型" prop="type">
        <template slot-scope="scope">
            <el-tag v-if="scope.row.type === 'CorePro Server'" size="medium">{{ scope.row.type }}</el-tag>
            <el-tag v-else-if="scope.row.type === 'DB'" size="medium" type="danger">{{ scope.row.type }}</el-tag>
            <el-tag v-else size="medium" type="success">{{ scope.row.type }}</el-tag>
          </template>
      </el-table-column>
      <el-table-column min-width="15%" label="创建时间" prop="create_time"></el-table-column>
      <el-table-column  min-width="15%" label="启用 / 禁用" prop="switch">
        <template v-slot="scope">
          <el-tooltip v-if="scope.row.switch === true" content="点击禁用设备传输通道"  placement="top">
            <el-switch size="small" v-model="scope.row.switch" @change="enablePath(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
          </el-tooltip>
          <el-tooltip v-else content="点击启用设备传输通道"  placement="top">
            <el-switch size="small" v-model="scope.row.switch" @change="enablePath(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column min-width="10%" label="数据库指针" prop="message_index"></el-table-column>
      <el-table-column min-width="10%" label="上行消息数" prop="message_number"></el-table-column>

      <el-table-column label="描述" min-width="10%" prop="description"></el-table-column>
      <el-table-column min-width="30%" label="操作">
        <template slot-scope="scope">
          <el-button type="text" @click="pathModify(scope.row)">修改</el-button>
          <el-button type="text" @click="getRealTimeMessage(scope.row)">消息详情</el-button>
          <el-button type="text" style="color: #FF0000" @click="deletePath(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>
    <!-- 新增转发弹出框 -->
    <el-dialog
    title="新增转发路径"
    :before-close="()=>{
      this.operationType='Save'
      this.dialogFormVisible = false
      }"
    :visible.sync="dialogFormVisible"
     custom-class="chile-device-box dialog-form"
     width="65%"
     >
      <el-form :model="form" label-position="left" label-width="120px" :rules="rules" ref="form">
        <el-form-item label="路径名称:" prop="name">
          <el-input v-if="operationType === 'Save'" type="text" v-model="form.name" size="small" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="路径名称" @blur="inputName"></el-input>
          <el-input v-else type="text" v-model="form.name" size="small" readonly></el-input>
        </el-form-item>
         <el-form-item label="路径描述:" prop="description">
          <el-input type="text" v-model="form.description" size="small" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="路径名称" @blur="inputName"></el-input>
        </el-form-item>
        <el-form-item label="转发类型:" prop="type">
          <el-select v-model="form.type" size="small" style="width: 100%" placeholder="请选择类型">
            <el-option v-for="item in typeList" :key="item.index" :value="item.value" :label="item.value" :disabled="item.disabled"></el-option>
          </el-select>
        </el-form-item>
        <div v-if="form.type==='第三方MQTT'">
          <el-form-item label="IP地址:" prop="ip">
            <el-input type="text" v-model="form.params.ip" size="small" oninput="value=value.replace(/[^0-9^.]/g, '')"  placeholder="MQTT服务器IP地址"></el-input>
          </el-form-item>
          <el-form-item label="端口号:" prop="port">
            <el-input type="number" v-model="form.params.port" size="small" placeholder="MQTT服务器端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名:" prop="username">
            <el-input type="text" v-model="form.params.username" size="small" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="password">
            <el-input show-password v-model="form.params.password"  size="small" placeholder="密码"></el-input>
          </el-form-item>
          <el-card>
            <el-form-item label="发布主题:" prop="shunts"  >
              <el-tabs>
                <el-tab-pane v-for="(shunts, key) in form.params.shunts" :key="key" :label="key">
                  <el-table :data="shunts">
                    <el-table-column label="ID" min-width="10%">
                      <template slot-scope="scope">
                        {{ scope.$index + 1}}
                      </template>
                    </el-table-column>
                    <el-table-column label="主题名" prop="shunt" min-width="80%">
                      <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.shunt" placeholder="请输入主题名"></el-input>
                      </template>
                    </el-table-column>

                    <el-table-column label="编辑" min-width="10%">
                      <template slot-scope="scope">
                        <el-button v-if="scope.$index !== shunts.length - 1" type="primary" size="small" @click="shunts.splice(scope.$index,1)">删除</el-button>
                        <el-button v-else type="success" size="small" @click="shunts.push({shunt: '' })">新增</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <!-- <el-input type="text" v-for="shunt in shunts" :key="shunt" placeholder="请输入发布主题"></el-input> -->
                </el-tab-pane>
              </el-tabs>
            </el-form-item>
          </el-card>

       </div>
       <div v-else-if="form.type==='CorePro Server'">

         <el-form-item label="数据类型:" prop="data_type">
            <el-input type="text" v-model="form.params.data_type" size="small"  @blur="inputName1" placeholder="CorePro 基础版的数据类型"></el-input>
          </el-form-item>
          <el-form-item label="数据类型ID:" prop="data_type_id">
            <el-input type="text" v-model="form.params.data_type_id" size="small" placeholder="CorePro 基础版的类型ID"></el-input>
          </el-form-item>
          <el-card>
            <el-form-item label="发布主题:" prop="shunts"  >
              <el-tabs>
                <el-tab-pane v-for="(shunts, key) in form.params.shunts" :key="key" :label="key">
                  <el-table :data="shunts">
                    <el-table-column label="ID" min-width="10%">
                      <template slot-scope="scope">
                        {{ scope.$index + 1}}
                      </template>
                    </el-table-column>
                    <el-table-column label="主题名" prop="shunt" min-width="80%">
                      <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.shunt" placeholder="请输入主题名"></el-input>
                      </template>
                    </el-table-column>

                    <el-table-column label="编辑" min-width="10%">
                      <template slot-scope="scope">
                        <el-button v-if="scope.$index !== shunts.length - 1" type="primary" size="small" @click="shunts.splice(scope.$index,1)">删除</el-button>
                        <el-button v-else type="success" size="small" @click="shunts.push({shunt: '' })">新增</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <!-- <el-input type="text" v-for="shunt in shunts" :key="shunt" placeholder="请输入发布主题"></el-input> -->
                </el-tab-pane>
              </el-tabs>
            </el-form-item>
          </el-card>
       </div>
       <div v-else-if="form.type==='DB'">
         <el-form-item label="数据库类型:" prop="db_type">
           <el-select v-model="form.params.db_type" size="small" style="width: 100%" >
            <el-option v-for="item in datatypeList" :key="item.index" :value="item.value" :label="item.value" :disabled="item.disabled"></el-option>
           </el-select>
         </el-form-item>
          <el-form-item label="服务器地址:" prop="ip">
            <el-input type="text" v-model="form.params.ip" size="small" oninput="value=value.replace(/[^0-9^.]/g, '')"  placeholder="服务器IP地址"></el-input>
          </el-form-item>
          <el-form-item label="服务器端口:" prop="port">
            <el-input type="number" v-model="form.params.port" size="small" placeholder="服务器端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名:" prop="username">
            <el-input type="text" v-model="form.params.username" size="small" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="password">
            <el-input show-password v-model="form.params.password"  size="small" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item label="数据库名:" prop="db_name"  >
            <el-input type="text" v-model="form.params.db_name"  size="small" placeholder="数据库名 or 数据库名:表名">
            </el-input>
          </el-form-item>
          <el-card>
            <el-form-item label="数据库表:" prop="shunts"  >
              <el-tabs>
                <el-tab-pane v-for="(shunts, key) in form.params.shunts" :key="key" :label="key">
                  <el-table :data="shunts">
                    <el-table-column label="ID" min-width="10%">
                      <template slot-scope="scope">
                        {{ scope.$index + 1}}
                      </template>
                    </el-table-column>
                    <el-table-column label="表名" prop="shunt" min-width="80%">
                      <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.shunt" placeholder="请输入数据库表名"></el-input>
                      </template>
                    </el-table-column>

                    <el-table-column label="编辑" min-width="10%">
                      <template slot-scope="scope">
                        <el-button v-if="scope.$index !== shunts.length - 1" type="primary" size="small" @click="shunts.splice(scope.$index,1)">删除</el-button>
                        <el-button v-else type="success" size="small" @click="shunts.push({shunt: '' })">新增</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <!-- <el-input type="text" v-for="shunt in shunts" :key="shunt" placeholder="请输入发布主题"></el-input> -->
                </el-tab-pane>
              </el-tabs>
            </el-form-item>
          </el-card>
       </div>

      </el-form>
      <el-row  slot="footer">
        <el-button type="success" size="small" @click="test('form',)" >测试</el-button>
        <el-button type="primary" size="small" @click="reset('form')" plain>重置</el-button>
        <el-button type="primary" size="small" @click="savePathInfo('form')">保存</el-button>

      </el-row>
    </el-dialog>

    <el-dialog title="数据转发状态" :visible.sync="dialogEdit" width="680px" height="420px" custom-class="chile-device-box dialog-form message-form">
      <el-table :data="subInfo">
        <el-table-column width="140" label="IP地址" prop="host">
        </el-table-column>
        <el-table-column width='120' label="端口号" prop="port">
        </el-table-column>
        <el-table-column label="消息主题"  prop="sub">
          <template v-slot="scope">
            <span >{{scope.row.sub}}</span>&nbsp;&nbsp;
            <el-button type="text" class="el-icon-document tag-read" @click="paste(scope.$index)"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-form>
         <el-form-item label="状态信息: " label-position="left" label-width="80px">
            <json-viewer
              :value="statusInfo"
              :expand-depth="5"
              copyable
              boxed
              sort
            ></json-viewer>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="数据消息详情" :visible.sync="dialogDetails" width="680px" height="420px" custom-class="chile-device-box dialog-form message-form">

      <el-form label-position="left" label-width="80px">
        <el-form-item label="消息详情: ">
          <json-viewer
            :value="realTimeMessage"
            :expand-depth="4"
            copyable
            boxed
            sort
          ></json-viewer>
        </el-form-item>
      </el-form>
    </el-dialog>
  </el-main>
</template>

<script>
import Clipboard from 'clipboard'
import { checkNull } from '../../../until/checkRules.js'
export default {
  data () {
    var dulapathname = (rule, value, callback) => {
      // 验证用户名是否存在.  一会再写
      if (value.length < 2) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else if (value.length > 15) {
        callback(new Error('长度在 2 到 15 个字符之间'))
      } else {
        callback()
        // this.$axios.post('/apis/device/path?select=1', {
        //   select_path: value
        // })
        //   .then(response => {
        //     if (response.data.is_indb === 1) {
        //       callback(new Error('该路径名称已经存在！'))
        //     } else {
        //       callback()
        //     }
        //   })
      }
    }
    return {
      dataFreshinterval: null,
      operationType: 'Save',
      realTimeMessage: {}, // 实时数据
      deleteBtn: true, // 批量删除按钮状态
      enableBtn: true, // 批量启用按钮状态
      disabledBtn: true, // 批量禁用按钮状态
      multipleSelection: [],
      loading: false,
      agent: {
        gateway_name: '',
        gateway_id: '',
        gateway_location: ''
      },
      sub_device_name: JSON.parse(sessionStorage.getItem('sub_device_name')),
      pathListTable: [
        // {
        //   index: 1,
        //   path_name:'test_1',
        //   switch: true,
        //   mesNumber: 1,
        //   createTime: '2018-08-09 16:19:55',
        //   type: 'CorePro'
        // }
      ],
      dialogFormVisible: false, // 新增转发弹出框
      drive_status_msg: '_',
      form: { // 新增转发表单
        name: 'test',
        type: '第三方MQTT',
        description: 'test',
        ip: '10.129.7.199',
        port: '1883',
        username: 'iot',
        password: 'iot123!',
        data_type: '',
        data_type_id: '',
        shunts: {},
        authentication: '',
        db_type: 'MySQL',
        db_name: 'test',
        params: {
          ip: '10.129.7.199',
          port: '1883',
          username: 'iot',
          password: 'iot123!',
          data_type: '',
          data_type_id: '',
          shunts: {},
          authentication: '',
          db_type: 'MySQL',
          db_name: 'test'
        }

      },
      rules: { // 新增转发表单验证
        name: [{ required: true, validator: checkNull, trigger: 'blur' },
          { validator: dulapathname, trigger: 'blur' }
        ],
        type: [{ required: true, validator: checkNull, trigger: 'blur' }],
        description: [{ required: true, validator: checkNull, trigger: 'blur' }],
        // params: [{ required: true, validator: checkNull, trigger: 'blur' }]
        // shunts: [{ required: true, validator: checkNull, trigger: 'blur' }],
        db_name: [{ required: true, validator: checkNull, trigger: 'blur' }],
        db_type: [{ required: true, validator: checkNull, trigger: 'blur' }],
        ip: [{ required: true, validator: checkNull, trigger: 'blur' }],
        port: [{ required: true, validator: checkNull, trigger: 'blur' }],
        username: [{ required: true, validator: checkNull, trigger: 'blur' }],
        password: [{ required: true, validator: checkNull, trigger: 'blur' }],
        data_type: [{ required: true, validator: checkNull, trigger: 'blur' }],
        data_type_id: [{ required: true, validator: checkNull, trigger: 'blur' }]
      },
      typeList: [
        { index: 0, value: '第三方MQTT' },
        { index: 1, value: 'CorePro Server' },
        { index: 2, value: 'DB' }
        // { index: 3, value: 'KAFKA' , disabled: true},
      ],
      datatypeList: [
        { index: 0, value: 'MySQL' },
        { index: 1, value: 'MsSQL' }
      ],
      dialogDetails: false, // 详情弹出框
      subInfo: [ // 详情信息
        {
          host: '127.0.0.1',
          port: 1883,
          sub: '/data/VirsualNWERobot/data'
        }
      ],
      statusInfo: {
        status_code: '200',
        count: 20,
        message: '驱动运行正常'
      },
      dialogEdit: false, // 编辑弹出框
      editRules: { // 编辑转发表单验证
        name: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        type: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ],
        topic: [
          {
            required: true, validator: checkNull, trigger: 'change'
          }
        ]
      }
    }
  },
  destroyed () {
    this.closeFresh()
  },
  mounted () {
  },
  created () {
    this.startFresh()
    this.getDataType()
    // this.getPathList()
    // this.dataFresh()
  },
  methods: {
    test (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/test', {
            params: this.form
          }).then(response => {
            if (response.data.status_code === 0) {
              _this.$Message.SuccessMessage(_this, response.data.message)
            } else {
              // _this.$Message.ErrorMessage(_this, response.data.message)
              alert(response.data.message)
              if (response.data.error_code === 1146) {
                _this.$Message.WarningAlert(_this, '是否需要自动建表？', '自动建表').then(
                  res => {
                    _this.$axios.post(
                      'apis/device/autoCreateDBTable',
                      {
                        db_tables: response.data.db_tables,
                        sub_device_name: _this.sub_device_name,
                        form: _this.form
                      }
                    ).then(
                      response => {
                        if (response.data.status_code === 0) {
                          _this.$Message.SuccessMessage(_this, response.data.message)
                        } else {
                          _this.$Message.ErrorMessage(_this, response.data.message)
                        }
                      }
                    ).catch(
                      error => {
                        console.error(error)
                      }
                    )
                  }

                ).catch(
                  error => {
                    console.error(error)
                  }
                )
              }
            }
          }).catch(error => {
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    getDataType () {
      var _this = this
      this.$axios.get('apis/device/getDataType', {
        params: {
          sub_device_name: this.sub_device_name
        }
      })
        .then(response => {
          if (response.data.status_code === 0) {
            this.form.params.shunts = response.data.shunts
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    toggleSelection (rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row)
        })
      } else {
        this.$refs.multipleTable.clearSelection()
      }
    },
    tableRowIndexArray (row) {
      // 设置row对象的index
      row.row.index = row.rowIndex
    },
    handleSelectionChange (val) {
      this.multipleSelection = val
      // 判断批量删除按钮的状态
      this.deleteBtn = this.multipleSelection.length <= 0
      this.enableBtn = this.multipleSelection.length <= 0
      this.disabledBtn = this.multipleSelection.length <= 0
    },
    //  批量启用或者禁用
    batchEnable (enable) {
      var _this = this
      let selectRows = this.multipleSelection
      let pathNameList = []
      for (let i in selectRows) {
        console.log(selectRows[i].switch)
        if (enable) {
          if (selectRows[i].switch === false) {
            pathNameList.push(selectRows[i].path_name)
          }
        } else {
          if (selectRows[i].switch === true) {
            pathNameList.push(selectRows[i].path_name)
          }
        }
      }
      if (enable) {
        if (pathNameList !== undefined & pathNameList.length > 0) {
        } else {
          _this.$Message.ErrorMessage(_this, '已全部启用')
          return
        }
      } else {
        if (pathNameList !== undefined & pathNameList.length > 0) {
        } else {
          _this.$Message.ErrorMessage(_this, '已全部禁用')
          return
        }
      }
      // console.log(sub_device_name_name_list)

      this.$axios.post('apis/device/pathEnable', {
        sub_device_name: this.sub_device_name,
        path_names: pathNameList,
        enable: enable
      })
        .then(function (response) {
          if (response.data.status_code === 0) {
            if (enable) {
              _this.flush_status(false)
            } else {
              _this.flush_status(false, 1500)
            }
            _this.$Message.SuccessMessage(_this, response.data.message)
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
            enable = false
          }
        })
        .catch(function (error) {
          console.log(error)
          enable = false
        })
    },
    // 批量删除
    bulkDelete () {
      var _this = this
      let selectRows = this.multipleSelection
      let pathNameList = []
      let enablePathList = []
      for (let i in selectRows) {
        if (selectRows[i].switch) {
          enablePathList.push(selectRows[i].path_name)
        } else {
          pathNameList.push(selectRows[i].path_name)
        }
      }
      // console.log(sub_device_name_name_list)
      if (pathNameList !== undefined & pathNameList.length > 0) {
        this.$Message.WarningAlert(this, '您确定要删除路径' + JSON.stringify(pathNameList) + '吗？', '转发路径删除').then(
          res => {
            this.$axios.post('apis/device/pathDelete', {
              sub_device_name: this.sub_device_name,
              path_names: pathNameList
            })
              .then(function (response) {
                if (response.data.status_code === 0) {
                  _this.$Message.SuccessMessage(_this, response.data.message)
                  _this.flush_status(false, 1000)
                } else {
                  _this.$Message.ErrorMessage(_this, response.data.message)
                }
              }
              )
              .catch(function (error) {
                console.log(error)
              })
          }
        )
      }
      setTimeout(() => {
        if (enablePathList !== undefined & enablePathList.length > 0) {
          this.$Message.WarningAlert(this, JSON.stringify(enablePathList) + '启用中不可删除')
        }
      }, 300)
    },
    inputName () {
      this.form.pubtopic = this.agent.gateway_name.toLowerCase() + '/' + this.sub_device_name.toLowerCase() + '/' + this.form.name.toLowerCase()
    },
    inputName1 () {
      this.form.datatopic = '/data/' + this.agent.gateway_id + '/' + this.form.datatype + '/data/gateway'
    },
    paste (index) {
      let sub = this.subInfo[0].sub
      let clipboard = new Clipboard('.tag-read', {
        text: function () {
          return sub
        }
      })
      // 复制成功
      clipboard.on('success', e => {
        // 复制成功的提示
        this.$Message.SuccessMessage(this, '复制成功')
        // 释放内存
        clipboard.destroy()
      })
      // 不支持复制
      clipboard.on('error', e => {
        // 复制失败的提示
        this.$Message.ErrorMessage(this, '复制失败')
        // 释放内存
        clipboard.destroy()
      })
    },
    flush_status (refresh = true, tm = 1) {
      var _this = this
      if (refresh) {
        this.getPathList()
        this.$axios.get('apis/device/showConfig', {
          params: {
            sub_device_name: this.sub_device_name,
            config_type: 'collect'
          }
        }) // 设备最新应用
          .then(response => {
            _this.drive_status_msg = response.data.drive_status_msg
          })
      } else {
        this.loading = true
        setTimeout(
          () => {
            this.getPathList()
          }, tm
        )
        this.$axios.get('apis/device/showConfig', {
          params: {
            sub_device_name: this.sub_device_name,
            config_type: 'collect'
          }
        }) // 设备最新应用
          .then(response => {
            _this.drive_status_msg = response.data.drive_status_msg
          })
        setTimeout(() => {
          this.loading = false
        }, 300)
      }
    },
    pathModify (row) {
      var _this = this
      this.$axios.get('apis/device/pathModify', {
        params: {
          sub_device_name: this.sub_device_name,
          path_name: row.path_name
        }
      }) // 设备协议清单
        .then(response => {
          if (response.data.status_code === 0) {
            this.form = response.data.path_config
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
          }
        })
      // this.getDataType()
      this.operationType = 'Modify'
      this.dialogFormVisible = true
    },
    getPathList () {
      var _this = this
      this.$axios.get('apis/device/pathList', {
        params: {
          sub_device_name: this.sub_device_name
        }
      }) // 设备协议清单
        .then(response => {
          if (response.data.status_code === 0) {
            this.pathListTable = response.data.path_list
          } else {
            _this.$Message.ErrorMessage(response.data.message)
          }

          // this.mesInfo = response.data.db.
        })
      // this.$axios.get('apis/agent/info/')
      //   .then(response => {
      //     this.agent.gateway_name = response.data.row_data[0].gateway_name
      //     this.agent.gateway_id = response.data.row_data[0].gateway_key
      //     this.agent.gateway_location = response.data.row_data[0].gateway_location

      //     this.form.params.shunts = response.data.row_data[0].gateway_name.toLowerCase() + '/' + this.sub_device_name.toLowerCase() + '/'
      //     this.form.datatopic = '/data/' + response.data.row_data[0].gateway_key + '/' + '{数据类型}/data/gateway'
      //   })
    },
    savePathInfo (formName) {
      var _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/pathSave', {
            sub_device_name: this.sub_device_name,
            params: this.form,
            operation_type: this.operationType
          }).then(response => {
            if (response.data.status_code === 0) {
              _this.$Message.SuccessMessage(_this, response.data.message)
              _this.dialogFormVisible = false
              _this.reset(formName)
              _this.getPathList()
            } else {
              _this.$Message.ErrorMessage(_this, response.data.message)
            }
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
    reset (formName) {
      this.$refs[formName].resetFields()
    },
    // test (formName) {
    //   var _this = this
    //   this.$refs[formName].validate((valid) => {
    //     if (valid) {
    //       this.$axios.get('apis/device/auth', {
    //         params: {
    //           authtype: _this.form.type,
    //           host: _this.form.ip,
    //           port: _this.form.port,
    //           username: _this.form.userName,
    //           pwd: _this.form.pwd
    //         }
    //       }).then(response => {
    //         if (response.data.status_code === 0) {
    //           _this.$Message.SuccessMessage(_this, response.data.message)
    //         } else {
    //           _this.$Message.ErrorMessage(_this, response.data.error)
    //         }
    //         this.operationType = 'Save'
    //       })
    //         .catch(function (error) {
    //           console.log(error)
    //         })
    //     } else {
    //       console.log('error submit!!')
    //       return false
    //     }
    //   })
    // },
    startFresh: function () {
      if (this.dataFreshinterval === null) {
        this.dataFreshinterval = setInterval(this.flush_status, 1000)
      }
    },
    closeFresh () {
      if (this.dataFreshinterval !== null) {
        clearInterval(this.dataFreshinterval)
        this.dataFreshinterval = null
      }
    },
    // 启用或者禁用
    enablePath (row) {
      var _this = this
      this.$axios.post('apis/device/pathEnable', {
        sub_device_name: JSON.parse(sessionStorage.getItem('sub_device_name')),
        path_names: [row.path_name],
        enable: row.switch
      })
        .then(function (response) {
          if (response.data.status_code === 0) {
            _this.$Message.SuccessMessage(_this, response.data.message)
            // _this.dataFresh()
          } else {
            _this.$Message.ErrorMessage(_this, response.data.message)
            row.switch = false
          }
        })
        .catch(function (error) {
          console.log(error)
          row.switch = false
        })
    },
    deletePath (row) {
      if (row.switch) {
        this.$Message.WarningAlert(this, '路径已经启动！请先关闭路径！', '路径删除')
      } else {
        this.$Message.WarningAlert(this, '您确定要删除' + row.path_name + '路径吗？', '路径删除').then(
          res => {
            var _this = this
            this.$axios.post('apis/device/pathDelete', {
              sub_device_name: this.sub_device_name,
              path_names: [row.path_name]
            })
              .then(function (response) {
                if (response.data.status_code === 0) {
                  _this.$Message.SuccessMessage(_this, response.data.message)
                  _this.flush_status(false)
                } else {
                  _this.$Message.ErrorMessage(_this, response.data.message)
                }
              })
              .catch(function (error) {
                console.log(error)
              })
          }
        )
      }
    },
    getRealTimeMessage () {
      this.dialogDetails = true
      var _this = this
      this.$axios.get('apis/device/getRealTimeMessage', {
        params: {
          sub_device_name: _this.sub_device_name
        }
      }).then(response => {
        if (response.data.status_code === 0) {
          this.realTimeMessage = response.data.real_time_message
        } else {
          _this.$Message.ErrorMessage(_this, response.data.message)
        }
      })
    }

  }
}
</script>

<style >

.message-form .el-form-item {
  margin: 25px 0px 10px 10px;
}
.row {
  padding: 10px 0px;
}
</style>
