<template>
  <el-main class="no-padding">
    <el-row  style="padding-left: 10px">

    </el-row>
    <el-row  class="el-row-margin row-self" >
       <!-- 模板接口信息 -->
      <el-tabs tab-position="top"  @tab-click="handleClick">
        <el-tab-pane  v-loading="loading" label="采集配置">
          <h4 class="title-style">({{template_name}})采集配置信息
          <el-button type="success" size="mini" icon="el-icon-refresh" @click="flushTemplateData()" plain>刷新</el-button>
          <el-button type="primary" size="small" style="float: right" @click="()=>{if (drive_status===false){dialogFormSMT=true}else{this.$Message.ErrorMessage(this, '请先关闭采集驱动')}}">修改配置</el-button>
          <el-button type="primary" size="small" style="float: right" @click="getTemplateList">关键字段提取</el-button>
          <span style="width: 500px"><h1 style="padding-right: 10px; color:#ff002fb3"> 采集驱动状态消息:{{ drive_status_msg }}</h1></span>
          </h4>
          <el-form :model="baseForm" label-width="120px" style="left: 1px; padding:0px 10px 0px 10px;" label-position="left" class="feature-card">
          <el-form-item v-for="(item ,index) of templateForm" :key="index" :label="item[0]">
            <div v-if="item[0] === '驱动状态' ">
              <div v-if="item[1] === false & status === false ">
                <el-tooltip content="串口被佔用或已不存在！"  placement="right-end">
                    <el-switch  stype='width: 30px' disabled v-model="item[1]" @change="alterCollectStatus(item[1], index)"
                      active-color="#409eff"
                      inactive-color="#DCDFE6">
                    </el-switch>
                </el-tooltip>
              </div>
              <div v-else>
                  <el-tooltip content="点击启用关闭设备采集驱动"  placement="right-end">
                    <el-switch  stype='width: 30px' v-model="item[1]" @change="alterCollectStatus(item[1], index)"
                      active-color="#409eff"
                      inactive-color="#DCDFE6">
                    </el-switch>
                  </el-tooltip>
              </div>
            </div>
            <div v-else-if="item[0] === '串口号'">
                <div v-if="drive_status === 0">
                    <el-tag v-if = "status === false" type="danger"> &nbsp;&nbsp;{{ item[1] }}&nbsp;&nbsp; </el-tag>
                    <el-tag v-else > &nbsp;&nbsp;{{ item[1] }}&nbsp;&nbsp; </el-tag>
                </div>
                <div v-else>
                  <el-tag type="success"> &nbsp;&nbsp;{{ item[1] }}&nbsp;&nbsp; </el-tag>
                </div>

            </div>
            <div v-else>
              <span>{{item[1]}}</span>
            </div>
          </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane v-loading="tableloading" label="实时数据">
          <h4 class="title-style">
            自动刷新
            <span v-if="beat === false">
              <el-tooltip content="点击开启自动刷新">
                <el-switch  stype='width: 30px; padding-left: 20px' v-model="beat"
                active-color="#409eff"
                inactive-color="#DCDFE6"
                @change="autoFreshData()">
              </el-switch>
            </el-tooltip>
            </span>

            <span v-else>
              <el-tooltip content="点击关闭自动刷新">
                <el-switch  stype='width: 30px; padding-left: 20px' v-model="beat"
                active-color="#409eff"
                inactive-color="#DCDFE6"
                @change="autoFreshData()">
              </el-switch>
            </el-tooltip>
            </span>

            <span v-if="beat === false">
              <el-tooltip  content="点击手动刷新"  placement="top-end">
                <el-button v-if="beat === false" type="success" size="mini" icon="el-icon-refresh" @click="flushTableData()" plain>手动刷新</el-button>
              </el-tooltip>
            </span>
            <span v-else>
              <el-tooltip  content="请先关闭自动刷新"  placement="top-end">
                <el-button type="primary" size="mini" plain>手动刷新</el-button>
              </el-tooltip>
            </span>

            <span style=" padding-right: 20px; padding-left: 30px">Total: {{Total}}</span>
            <span style=" padding-right: 20px">Row: {{Row}}</span>
            <span style=" padding-right: 20px">Time: {{timestamp}}</span>

            <el-button type="primary" size="small" style="float: right" plain @click="()=>{dialogFormApi=true}">查看设备API</el-button>
          </h4>
          <el-tabs v-if="templateForm[1][1] ==='SMT'">
            <el-tab-pane v-for="(item, key) in formatData" :key="key" :label="key" :name="key.$index">
              <el-table height="500" :row-class-name="tableRowClassName" border :data="formatData[key]">
                <el-table-column v-for="(value, dataKey) in formatData[key][0] " :key="dataKey" :label="dataKey" :prop="dataKey">
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    <!-- 获取API -->
    <el-dialog title="设备API" :visible.sync="dialogFormApi" width="800px" custom-class="chile-device-box dialog-form">
      <el-form  label-position="left" label-width="100px">
        <el-form-item label="URI地址:" prop="uri">
          <el-input type="text" v-model="uri"  style="width:100%" size="small" placeholder="设备URI地址"></el-input>
        </el-form-item>
      </el-form>
      <el-row  slot="footer">
        <!-- <el-button type="primary" size="mini">Open</el-button> -->
        <el-button type="success" size="mini" class="tag-read" @click="doCopy" >Copy</el-button>
      </el-row>
    </el-dialog>
    <!-- 修改采集配置 -->
    <el-dialog :title="'协议接口配置('+template_name+')'" :visible.sync="dialogFormSMT" width="680px" custom-class="chile-device-box dialog-form">
      <smt-form  :template_name ="template_name" :device_type="device_type" :file_type="file_type" :category="drive_type" :flushTemplate='flushTemplateData'
        @CloseDialog="closeDialogSmt" >
      </smt-form>

    </el-dialog>
    <!-- 特征提取 -->
    <el-dialog title="属性数据提取" :visible.sync="dialogFormMap" width="800px" custom-class=" dialog-form ">

      <el-alert
            title="提示: 属性数据提取确认将作为数据转发模块的输出设备属性模板, 不选则默认所有！"
            type="warning"
            show-icon>
      </el-alert>
      <div style="text-align: center">
        <el-tabs>
          <el-tab-pane v-for="(item, key) in selected_features" :key="key" :label="key">
            <!-- <template slot-scope="scope"> -->
              <el-transfer v-model="selected_features[key]" :data="total_features[key]"
              style="text-align: left; display: inline-block"
              filterable
              filter-placeholder="按属性名搜索"
              :titles="['未提取设备源数据', '已提取关键字段']"
              :button-texts="['撤销', '选择']"
              ></el-transfer>
            <!-- </template> -->

          </el-tab-pane>
        </el-tabs>

      </div>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="dialogFormMap=false">取消</el-button>
        <el-button type="primary" size="small" @click="featureExtraction">确定</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
import Clipboard from 'clipboard'
import smtForm from '../components/smtForm.vue'
// import { getData } from '../../../until/smt.js'
// import func from '../../../../vue-temp/vue-editor-bridge'
export default {

  data () {
    return {
      total_features: [{
        key: 'Mod',
        label: 'Mod',
        disabled: false
      }],
      timestamp: '',
      drive_type: '',
      device_type: '',
      file_type: '',
      dialogFormSMT: false,
      dataFreshinterval: null,
      drive_status: true,
      status: false,
      selected_features: [],
      tableloading: false,
      beat: true,
      loading: false,
      uri: 'null',
      Total: 0,
      Row: 0,
      dialogFormApi: false,
      dialogFormMap: false,
      sub_device_name: JSON.parse(window.sessionStorage.getItem('sub_device_name')),
      template_name: '',
      drive_status_msg: '',
      baseForm: {

      },
      // test: [],
      formatData: {
      },
      templateForm: [

      ],
      featureForm: {
        max: 28,
        min: 22,
        avg: 25
      },
      tableData: [

      ],
      count: 0
    }
  },
  components: {
    smtForm
  },
  mounted () {
    // if (this.dataFreshinterval === null) {
    //   this.dataFresh()
    // }
  },
  created () {
    this.flushTemplateData()
    this.flushTableData(false)
  },
  destroyed () {
    if (this.dataFreshinterval !== null) {
      clearInterval(this.dataFreshinterval)
      this.dataFreshinterval = null
    }
  },
  methods: {
    handleClick (tab, event) {
      if (tab.$options.propsData.label === '实时数据') {
        this.autoFreshData()
      } else {
        if (this.dataFreshinterval !== null) {
          clearInterval(this.dataFreshinterval)
          this.dataFreshinterval = null
        }
      }
    },
    closeDialogSmt (val) {
      this.dialogFormSMT = val
      this.$emit('dump')
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex === 0) {
        return 'success-row'
      } else if (rowIndex === 1) {
        return 'success-row'
      }
      return ''
    },
    manualFresh () {
      this.flushTableData()
    },
    autoFreshData () {
      this.tableloading = true
      if (this.beat & this.drive_status) {
        if (this.dataFreshinterval === null) {
          this.dataFresh()
        }
      } else {
        if (this.dataFreshinterval !== null) {
          clearInterval(this.dataFreshinterval)
          this.dataFreshinterval = null
        }
      }
      setTimeout(() => {
        this.tableloading = false
      }, 300)
    },
    dataFresh: function () {
      this.dataFreshinterval = setInterval(this.flushTableData, 500)
    },
    getRowKeys (row) {
      return row.property
    },
    getTemplateList () {
      if (this.drive_status === false) {

      } else {
        this.$Message.ErrorMessage(this, '请先关闭采集驱动')
        return
      }
      this.$axios.get('apis/device/featureExtraction/', {
        params: {
          template_name: this.template_name
          // device_name: this.sub_device_name
        }
      }) // 最近一条数据
        .then(response => {
          if (response.data.status_code === 1) {
            this.$Message.ErrorMessage(this, response.data.error)
          } else {
            this.selected_features = response.data.selected_features
            this.total_features = response.data.total_features
            this.dialogFormMap = true
          }
        })
    },
    featureExtraction () {
      var _this = this
      this.$axios.post('apis/device/featureExtraction/', {
        template_name: this.template_name,
        selected_features: this.selected_features
      })
        .then(response => {
          if (response.data.status_code === 0) {
            _this.$Message.SuccessMessage(_this, response.data.message)
            _this.dialogFormMap = false
          } else {
            _this.$Message.SuccessMessage(_this, response.data.message)
          }
        }
        )
      _this.dialogFormMap = false
    },
    load () {
      this.count += 2
    },
    doCopy () {
      var _this = this
      let clipboard = new Clipboard('.tag-read', {
        text: function () {
          return _this.uri
        }
      })
      // 复制成功
      clipboard.on('success', e => {
        // 复制成功的提示
        // this.$Message.SuccessMessage(this, '复制成功');
        // 释放内存
        clipboard.destroy()
        this.dialogFormApi = false
      })
      // 不支持复制
      clipboard.on('error', e => {
        // 复制失败的提示
        this.$Message.ErrorMessage(this, '复制失败')
        // 释放内存
        clipboard.destroy()
      })
    },
    alterCollectStatus (enable, index) { // 改变驱动状态
      this.templateForm[index][1] = index
      this.sendEnable(enable)
      setTimeout(() => {
        this.flushTemplateData()
      }, 1000)
      this.flushTableData(false)
    },
    sendEnable (val) {
      var _this = this
      this.$axios.post('apis/device/collectEnable/', {
        enable: val,
        sub_device_name: this.sub_device_name
      })
        .then(response => {
          if (response.data.status_code === 0) {
            _this.$Message.SuccessMessage(_this, response.data.message)
          } else {
            this.beat = false
            _this.$Message.ErrorMessage(_this, response.data.message)
          }
          // console.log(response);
        })
    },
    flushTableData (refresh = true) {
      if (refresh) {} else {
        this.tableloading = true
      }

      this.$axios.get('apis/device/data', {
        params: {
          sub_device_name: this.sub_device_name,
          template_name: this.template_name,
          // template_name: JSON.parse(sessionStorage.getItem('template_'+this.sub_device_name)),
          row: 0
        }
      }) // 最近一条数据
        .then(response => {
          if (response.data.status_code === 1) {

          } else {
            if (refresh) {
              this.formatData = response.data.formatData
              this.Total = response.data.Total
              this.Row = response.data.Row
              this.uri = response.data.URI
              this.timestamp = response.data.time
            } else {
              this.tableData = response.data.tableData
              // console.log(JSON.stringify(this.tableData))
              this.formatData = response.data.formatData
              this.Total = response.data.Total
              this.Row = response.data.Row
              this.uri = response.data.URI
              this.timestamp = response.data.time
            }
          }
        })
      if (refresh) {} else {
        setTimeout(() => {
          this.tableloading = false
        }, 300)
      }
    },
    flushTemplateData () {
      var _this = this
      this.loading = true
      this.$axios.get('apis/device/showConfig', {
        params: {
          sub_device_name: this.sub_device_name,
          config_type: 'collect'
        }
      }) // 设备最新应用
        .then(response => {
          _this.templateForm = response.data.db
          console.log(_this.templateForm)
          _this.drive_type = _this.templateForm[1][1]
          _this.device_type = _this.templateForm[2][1]
          _this.file_type = _this.templateForm[4][2]
          console.log(_this.drive_type, _this.device_type, _this.file_type)
          _this.template_name = response.data.template_name
          _this.status = response.data.status
          _this.drive_status = response.data.drive_status
          _this.drive_status_msg = response.data.drive_status_msg
          // window.sessionStorage.setItem('template_'+this.sub_device_name, JSON.stringify(response.data.template_name));
          // this.flushTableData()
        })
      setTimeout(() => {
        this.loading = false
      }, 300)
      // this.flushTableData()
    }
    // timer() {
    //   return setTimeout(()=>{
    //         this.flushTableData()
    //     },3000)
    // },
  }
  // watch: {
  //     tableData() {
  //       this.timer()
  //     }

  // },
  // destroyed() {
  //   clearTimeout(this.timer)
  // }
}
</script>

<style >
  .el-table--border:after,
  .el-table--group:after,
  .el-table:before {
      background-color: white;
  }

  .el-table--border,
  .el-table--group {
      border-color: ivory;
  }

  .el-table td,
  .el-table th.is-leaf {
          border-bottom: 1px solid ivory;
  }

  .el-table--border th,
  .el-table--border th.gutter:last-of-type {
          border-bottom: 1px solid ivory;
  }

  .el-table--border td,
  .el-table--border th {
          border-right: 1px solid ivory;
  }
  .row-self .table-card {
    margin: 15px 10px 0px 10px;
  }
  .el-transfer {
      font-size: 14px;
      padding: 15px 0px 0px 0px;
  }
  .row-self .el-card {
      border: 1px solid #b4b9c5;
  }
  .el-transfer-panel {
      border: 1px solid #42675096;
  }
  .el-transfer__button:first-child {
      width: 85px;
  }
  .el-transfer__button:nth-child(2) {
      width: 85px;
  }
  .el-transfer__buttons {
      padding: 0px 20px;
  }
  .el-transfer-panel {
      width: 255px;
  }
  .el-table .warning-row {
    background: green;
  }

  .el-table .success-row {
    background: wheat;
  }
</style>
