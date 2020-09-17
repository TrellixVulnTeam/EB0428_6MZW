<template>
  <el-main class="no-padding">
    <el-alert
      title="提示: 每个设备最多可配置四条转发路径"
      type="warning"
      show-icon>
    </el-alert>
    <div 
      v-loading="loading"
     >
    <el-row class="row-padding row" >
      <el-button type="primary" size="small" @click="dialogFormVisible = true">新增</el-button>
      <el-button type="success" size="small" @click="flush_status()" icon="el-icon-refresh" plain>刷新</el-button>        
      <span style="width: 500px"><h style="padding-right: 10px; color:#ff002fb3"> {{ drive_status_msg }}</h></span>
    </el-row>
    <el-table :data="tableData">
      <!-- <el-table-column label="序号" prop="index"></el-table-column> -->
      <el-table-column min-width="15%" label="路径名称" prop="addressName"></el-table-column>
      <el-table-column min-width="15%" label="类型" prop="type">
        <template slot-scope="scope">
            <el-tag v-if="scope.row.type === 'CorePro Server'" size="medium">{{ scope.row.type }}</el-tag>
            <el-tag v-else-if="scope.row.type === 'DB'" size="medium" type="danger">{{ scope.row.type }}</el-tag>
            <el-tag v-else size="medium" type="success">{{ scope.row.type }}</el-tag>
          </template>
      </el-table-column>
      <el-table-column min-width="15%" label="创建时间" prop="createTime"></el-table-column>
      <el-table-column  min-width="15%" label="启用 / 禁用" prop="switch">
        <template v-slot="scope">
          <el-tooltip content="点击启用禁用设备传输通道"  placement="top">
            <el-switch size="small" v-model="scope.row.switch" @change="chooseStatus(scope.row)" active-color="#13ce66" inactive-color="#DCDFE6"></el-switch>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column min-width="10%" label="上行消息数" prop="mesNumber"></el-table-column>

      <!-- <el-table-column label="描述" prop="description"></el-table-column> -->
      <el-table-column min-width="30%" label="操作">
        <template slot-scope="scope">
          <el-button type="text" @click="status(scope.row)">查看状态</el-button>
          <el-button type="text" @click="msg(scope.row)">消息详情</el-button>
          <el-button type="text" style="color: #FF0000" @click="deleteRow(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>
    <!-- 新增转发弹出框 -->
    <el-dialog title="新增转发路径" :visible.sync="dialogFormVisible" custom-class="chile-device-box dialog-form" width="560px">
      <el-form :model="form" label-position="left" label-width="120px" :rules="rules" ref="form">
        <el-form-item label="路径名称:" prop="name">
          <el-input type="text" v-model="form.name" size="small" oninput="value=value.replace(/[^0-9^A-Z^a-z]/g, '')" placeholder="路径名称" @blur="inputName"></el-input>
        </el-form-item>
        <el-form-item label="转发类型:" prop="type">
          <el-select v-model="form.type" size="small" style="width: 100%" placeholder="请选择类型">
            <el-option v-for="item in typeList" :key="item.index" :value="item.value" :label="item.value" :disabled="item.disabled"></el-option>
          </el-select>
        </el-form-item>
        <div v-if="form.type==='第三方MQTT'">
          <el-form-item label="IP地址:" prop="ip">
            <el-input type="text" v-model="form.ip" size="small" oninput="value=value.replace(/[^0-9^.]/g, '')"  placeholder="MQTT服务器IP地址"></el-input>
          </el-form-item>
          <el-form-item label="端口号:" prop="port">
            <el-input type="number" v-model="form.port" size="small" placeholder="MQTT服务器端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名:" prop="userName">
            <el-input type="text" v-model="form.userName" size="small" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="pwd">
            <el-input show-password v-model="form.pwd"  size="small" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item label="发布主题:" prop="pubtopic"  >
            <el-input type="text" v-model="form.pubtopic"  size="small" placeholder="发布的MQTT Topic主题">
            </el-input>
          </el-form-item>
       </div>
       <div v-else-if="form.type==='CorePro Server'">
         
         <el-form-item label="数据类型:" prop="datatype">
            <el-input type="text" v-model="form.datatype" size="small"  @blur="inputName1" placeholder="CorePro 基础版的数据类型"></el-input>
          </el-form-item>
          <el-form-item label="数据类型ID:" prop="datatypeid">
            <el-input type="text" v-model="form.datatypeid" size="small" placeholder="CorePro 基础版的类型ID"></el-input>
          </el-form-item>
          <el-form-item label="消息主题:" prop="datatopic">
            <el-input type="text" v-model="form.datatopic" size="small" placeholder="CorePro 基础版的消息主题"></el-input>
          </el-form-item>
       </div>
       <div v-else-if="form.type==='DB'">
         <el-form-item label="数据库类型:" prop="databasetype">
           <el-select v-model="form.databasetype" size="small" style="width: 100%" >
            <el-option v-for="item in datatypeList" :key="item.index" :value="item.value" :label="item.value" :disabled="item.disabled"></el-option>
           </el-select>
         </el-form-item>
          <el-form-item label="服务器地址:" prop="dbip">
            <el-input type="text" v-model="form.dbip" size="small" oninput="value=value.replace(/[^0-9^.]/g, '')"  placeholder="服务器IP地址"></el-input>
          </el-form-item>
          <el-form-item label="服务器端口:" prop="dbport">
            <el-input type="number" v-model="form.dbport" size="small" placeholder="服务器端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名:" prop="dbuserName">
            <el-input type="text" v-model="form.dbuserName" size="small" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="dbpwd">
            <el-input show-password v-model="form.dbpwd"  size="small" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item label="数据库名:" prop="dbname"  >
            <el-input type="text" v-model="form.dbname"  size="small" placeholder="数据库名 or 数据库名:表名">
            </el-input>
          </el-form-item>
       </div>
       <div v-if="form.type==='Result Down'">
          <el-form-item label="IP地址:" prop="ip">
            <el-input type="text" v-model="form.ip" size="small" oninput="value=value.replace(/[^0-9^.]/g, '')"  placeholder="MQTT服务器IP地址"></el-input>
          </el-form-item>
          <el-form-item label="端口号:" prop="port">
            <el-input type="number" v-model="form.port" size="small" placeholder="MQTT服务器端口号"></el-input>
          </el-form-item>
          <el-form-item label="用户名:" prop="userName">
            <el-input type="text" v-model="form.userName" size="small" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="pwd">
            <el-input show-password v-model="form.pwd"  size="small" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item label="发布主题:" prop="pubtopic"  >
            <el-input type="text" v-model="form.pubtopic"  size="small" placeholder="下发的MQTT Topic主题">
            </el-input>
          </el-form-item>
       </div>

      </el-form>
      <el-row  slot="footer">
        <el-button  v-if="form.type == '第三方MQTT'" type="success" size="small" @click="test('form')" >测试</el-button>
        <el-button type="primary" size="small" @click="reset('form')" plain>重置</el-button>
        <el-button type="primary" size="small" @click="save('form')">保存</el-button>

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
            :value="mesInfo"
            :expand-depth="1"
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
import Clipboard from 'clipboard';
import { checkNull } from '../../../until/checkRules.js'
export default {
  data() {
     var dulapathname = (rule, value, callback) => {
        // 验证用户名是否存在.  一会再写
        if (value.length < 2) {
          callback(new Error('长度在 2 到 15 个字符之间'))
        } else if (value.length > 15) {
          callback(new Error('长度在 2 到 15 个字符之间'))
        } else {
          this.$axios.post('/apis/device/path?select=1', {
            select_path: value
          })
            .then(response => {
              if (response.data.is_indb === 1) {
                callback(new Error('该路径名称已经存在！'))
              } else {
                callback();
              }
            })
        }
      }
    return {
      loading: false,
      agent:{
        gateway_name:"" ,
        gateway_id:"",
        gateway_location:""
      },
      subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
      tableData: [
        // {
        //   index: 1,
        //   addressName:'test_1', 
        //   switch: true,
        //   mesNumber: 1,
        //   createTime: '2018-08-09 16:19:55',
        //   type: 'CorePro'
        // }
      ],
      dialogFormVisible: false, // 新增转发弹出框
      drive_status_msg:"_",
      form: { // 新增转发表单
        databasetype: "MySQL",
        datatype: '',
        datatypeid: '',
        datatopic: '',
        name: '',
        type: '',
        pubtopic: "/edgebox/test",
        authentication: '',
        ip: '10.129.7.199',
        port: '1883',
        userName: 'iot',
        pwd: 'iot123!',
        dbip: '127.0.0.1',
        dbport: '3306',
        dbuserName: 'root',
        dbpwd: '123456',
        dbname: 'test',
      },
      rules: { // 新增转发表单验证
        name: [{required: true, validator: checkNull, trigger: 'blur'},
              { validator: dulapathname, trigger: 'blur'}],
        type: [{required: true, validator: checkNull, trigger: 'blur'}],
        pubtopic: [{required: true, validator: checkNull, trigger: 'blur'}],
        ip: [{required: true, validator: checkNull, trigger: 'blur'}],
        port: [{required: true, validator: checkNull, trigger: 'blur'}],
        userName: [{required: true, validator: checkNull, trigger: 'blur'}],
        pwd: [{required: true, validator: checkNull, trigger: 'blur'}],
        datatype: [{required: true, validator: checkNull, trigger: 'blur'}],
        datatypeid: [{required: true, validator: checkNull, trigger: 'blur'}],
        datatopic: [{required: true, validator: checkNull, trigger: 'blur'}],
      },
      typeList: [
        { index: 0, value: '第三方MQTT' },
        { index: 1, value: 'CorePro Server' },
        { index: 2, value: 'DB' },
        { index: 3, value: 'Result Down' },
        // { index: 3, value: 'KAFKA' , disabled: true},
      ],
      datatypeList: [
        { index: 0, value: 'MySQL' },
        { index: 1, value: 'MongoDB' },
      ],
      dialogDetails: false, // 详情弹出框
      subInfo:[ // 详情信息
        {
          host: '127.0.0.1',
          port: 1883,
          sub: '/data/VirsualNWERobot/data'
        }
      ],
      statusInfo:{
        status_code: "200",
        count: 20,
        message: "驱动运行正常"
      },
     
      mesInfo: { // 消息详情
        Temperature: 123,
        humidity3: 1212,
        humidity2: 456,
        humidity1: 123,

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
      },
    }
  },
  mounted() {
  },
  created() {
    this.getData();
  },
  methods: {
    inputName() {
      this.form.pubtopic = this.agent.gateway_name.toLowerCase() + "/" + this.subdevice_name.toLowerCase() + "/"+ this.form.name.toLowerCase();
    },
    inputName1() {
      this.form.datatopic = "/data/"+this.agent.gateway_id+"/" +this.form.datatype+"/data/gateway"
    },
    msg(row) {
      this.dialogDetails = true;
      this.mesInfo = row.path_msg
    },
    paste(index) {
      let sub = this.subInfo[0].sub;
      let clipboard = new Clipboard('.tag-read', {
            text: function() {
                return sub;
            }
      });
       // 复制成功
       clipboard.on('success', e => {
          // 复制成功的提示
          this.$Message.SuccessMessage(this, '复制成功');
          // 释放内存
          clipboard.destroy()
        })
        // 不支持复制
        clipboard.on('error', e => {
          // 复制失败的提示
          this.$Message.ErrorMessage(this, '复制失败');
          // 释放内存
          clipboard.destroy()
        });
    },
    flush_status() {
      this.loading = true
      this.getData()
      setTimeout(() =>{
            this.loading = false
        },300)

    },
    status(row) {
      this.dialogEdit = true
      this.$axios.get("apis/device/path/info",{
         params:{            
                subdevice: this.subdevice_name,
                path_name: row.addressName,
                path_type: row.type
              }
        }) //设备协议清单
        .then(response => {
          this.statusInfo = response.data.status;
          this.subInfo = response.data.sub
        })

    },
    getData() {
      this.$axios.get("apis/device/path",{
         params:{            
                subdevice: this.subdevice_name
              }
        }) //设备协议清单
        .then(response => {
          this.tableData = response.data.db;
          // this.mesInfo = response.data.db.
        })
      this.$axios.get("apis/agent/info/",)
      .then(response => {
        this.agent.gateway_name = response.data.row_data[0].gateway_name;
        this.agent.gateway_id = response.data.row_data[0].gateway_key;
        this.agent.gateway_location = response.data.row_data[0].gateway_location;

        this.form.pubtopic = response.data.row_data[0].gateway_name.toLowerCase() + "/" + this.subdevice_name.toLowerCase() + "/"
        this.form.datatopic="/data/"+response.data.row_data[0].gateway_key+"/" +"{数据类型}/data/gateway"

      })
    },
    save(formName) {
      var _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.post('apis/device/path', {
            subdevice: this.subdevice_name,
            path_type: this.form.type,
            params: this.form 
          }).then(response => {
            if(response.data.status_code === 0){
                this.$Message.SuccessMessage(this, response.data.message);
            }
            else{
                this.$Message.ErrorMessage(this, response.data.error);
            }
            this.dialogFormVisible = false;
            _this.reset(formName);
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
    reset(formName) {
       this.$refs[formName].resetFields();
    },
    test(formName) {
      var _this = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.get('apis/device/auth', {
            params: {
              authtype: _this.form.type,
              host: _this.form.ip,
              port: _this.form.port,
              username: _this.form.userName ,
              pwd: _this.form.pwd
            }
          }).then(response => {
            if(response.data.status_code === 0){
                _this.$Message.SuccessMessage(_this, response.data.message);
            }
            else{
                _this.$Message.ErrorMessage(_this, response.data.error);
            }
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
    // 启用或者禁用
    chooseStatus(row) {
      var _this = this;
      this.$axios.post('apis/device/path/enable', {
          subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
          path_name: row.addressName,
          enable: row.switch
        })
        .then(function (response) {
          if(response.data.status_code === 0){
              _this.$Message.SuccessMessage(_this, response.data.message);
          }
          else{
              _this.$Message.ErrorMessage(_this, response.data.message);
              row.switch = false
          }
        })
        .catch(function (error) {
          console.log(error);
          row.switch = false
        });
    },
    deleteRow(row) {
      console.log(row.switch)
      if(row.switch){
        this.$Message.WarningAlert(this,'路径已经启动！请先关闭路径！','路径删除')
      }else{
        this.$Message.WarningAlert(this,'您确定要删除此路径吗？','路径删除').then(
          res => {
            var _this = this;
            this.$axios.post('apis/device/path/delete', {
                subdevice_name: JSON.parse(sessionStorage.getItem('subdevice')),
                path_name: row.addressName,
              })
              .then(function (response) {
                if(response.data.status_code === 0){
                    _this.$Message.SuccessMessage(_this, response.data.message);
                    _this.flush_status()
                }
                else{
                    _this.$Message.ErrorMessage(_this, response.data.message);
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          }
        );
      }
      
    },
    
  },
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
