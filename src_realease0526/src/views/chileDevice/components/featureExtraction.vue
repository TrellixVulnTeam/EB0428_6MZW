<template>
  <el-main class="no-padding">
    <el-row  style=" padding-left: 10px">
      <el-col >
        <el-button type="primary" size="small" style="float: left" @click="getVarList">关键字段提取</el-button>
        <el-button type="primary" size="small" plain @click="dialogFormApi=true">查看设备API</el-button>
        <!-- <span style="width: 500px"><h style="padding-right: 10px">Row</h></span> -->
      </el-col>
    </el-row>
    <el-row  class="el-row-margin row-self" >
       <!-- 模板接口信息 -->
      <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" style="width: 34%">
          <el-card
            v-loading="loading"
            class="table-card"
            shadow="hover"
            size="small">
            <h4 class="title-style">模板({{templatename}})接口信息
            <el-button type="success" size="mini" icon="el-icon-refresh" @click="flushtemplatedata()" plain>刷新</el-button>
            </h4>
            <el-form :model="baseForm" label-width="120px" style="left: 1px" label-position="left" class="feature-card">
            <el-form-item v-for="(item ,index) of templateForm" :key="index" :label="item[0]">
              <div v-if="item[0] === '驱动状态' ">
                <el-tooltip content="点击启用关闭设备采集驱动"  placement="right-end">
                    <el-switch stype='width: 30px' v-model="item[1]" @change="chooseStatus(item[1])"
                      active-color="#409eff"
                      inactive-color="#DCDFE6">
                    </el-switch>
                </el-tooltip>
              </div>
              <div v-else>
                <span>{{item[1]}}</span>
              </div>
            </el-form-item>
            </el-form>
        </el-card>
      </el-col>
      <el-col  :xs="12" :sm="12" :md="12" :lg="12" :xl="12" style="width: 64% ">
        <el-card
          v-loading="tableloading"
          class="table-card"  shadow="hover" style="height: 475px">
          <h4 class="title-style">
            设备属性
            <el-button type="success" size="mini" icon="el-icon-refresh" @click="flushtabledata()" plain>刷新</el-button>
            <span style="float: right; padding-right: 20px">Total: {{Total}}</span>
            <span style="float: right; padding-right: 20px">Row: {{tableData.length}}</span>
          </h4>
          <el-table :data="tableData" tooltip-effect="dark"  :row-key="getRowKeys" class="feature-card" style="width: 100%"  height="400">
            <!-- <el-table-column type="selection" :reserve-selection="true" width="80"></el-table-column> -->
            <el-table-column label="property" prop="property" style="width: 25% "></el-table-column>
            <el-table-column label="value" prop="value" style="width: 20% "></el-table-column>
            <el-table-column label="create_time" prop="create_time" style="width: 48% " ></el-table-column>

          </el-table>
          <!-- <div> -->
          <!-- <ul class="infinite-list" v-infinite-scroll="load" style="overflow:auto">
            <li v-for="i in count" class="infinite-list-item" :key="i">{{ i }}

            </li>
          </ul>
          </div> -->

        </el-card>
      </el-col>
    </el-row>

    <el-row style="padding-top:2em">
      <el-card>
        <echarts ref="echarts"></echarts>
      </el-card>
    </el-row>

    <el-dialog title="设备API" :visible.sync="dialogFormApi" width="680px" custom-class="chile-device-box dialog-form">
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
    <el-dialog title="属性数据提取" :visible.sync="dialogFormMap" width="680px" custom-class="chile-device-box dialog-form ">
      <!-- <el-form  label-position="left" >
        <el-form-item  prop="format">
          <json-viewer
            :value="formatData"
            :expand-depth="5"
            copyable
            boxed
            sort
          ></json-viewer>
        </el-form-item>
      </el-form> -->
      <el-alert
            title="提示: 属性数据提取确认将作为数据转发模块的输出设备属性模板, 不选则默认所有！"
            type="warning"
            show-icon>
      </el-alert>
      <div style="text-align: center">
        <el-transfer v-model="value" :data="data"
        style="text-align: left; display: inline-block"
        filterable
        filter-placeholder="按属性名搜索"
        :titles="['设备源数据', '关键字段']"
        :button-texts="['撤销', '选择']"
        ></el-transfer>
      </div>
      <el-row  slot="footer">
        <el-button type="default" size="small" @click="dialogFormMap=false">取消</el-button>
        <el-button type="primary" size="small" @click="feature">确定</el-button>
      </el-row>
    </el-dialog>
  </el-main>
</template>

<script>
import Clipboard from 'clipboard'
import echarts from '../../gatewayManage/components/echarts.vue'

export default {

  data () {
    return {
      data: [{
        key: 'Mod',
        label: 'Mod',
        disabled: false
      }],
      value: [],
      tableloading: false,
      loading: false,
      uri: 'null',
      Total: 0,
      dialogFormApi: false,
      dialogFormMap: false,
      subdevice_name: JSON.parse(window.sessionStorage.getItem('subdevice')),
      templatename: '',
      baseForm: {

      },
      formatData: {
        // Temperature: 123,
        // humidity3: 1212,
        // humidity2: 456,
        // humidity1: 123
      },
      templateForm: [
        // ["模板名称", "HC33A2-00"],
        ['驱动名称', 'Demo'],
        ['驱动类型', 'Modbus-RTU'],
        ['驱动状态', true],
        ['Slave地址', '01'],
        ['串口号', 'COM3'],
        ['波特率', '9600 bps'],
        ['奇偶校验', 'None,无校验'],
        ['数据位', '8 bit'],
        ['停止位', '2 bit'],
        ['回复超时', '0.5 second'],
        ['读写周期', '3.0 second']
      ],
      featureForm: {
        max: 28,
        min: 22,
        avg: 25
      },
      tableData: [
        // {property: "Temperature",value: 28},
        // {property: "humidity",value: 40},
        // {property: "humidity",value: 40},
        // {property: "Temperature",value: 28},
      ],
      count: 0
    }
  },
  mounted () {

  },
  created () {
    this.flushtemplatedata()
    // this.flushtabledata();
  },
  mounted(){
    this.$refs["echarts"].barPlus()
  },
  components:{
    echarts
  },
  methods: {
    getRowKeys (row) {
      return row.property
    },
    getVarList () {
      this.$axios.get('apis/drive/varlist/', {
        params: {
          template_name: this.templatename,
          device_name: this.subdevice_name
        }
      }) // 最近一条数据
        .then(response => {
          if (response.data.status_code === 1) {
            this.$Message.ErrorMessage(this, response.data.error)
          } else {
            this.value = response.data.varlist
            this.dialogFormMap = true
          }
        })
    },
    feature () {
      var _this = this
      this.$axios.post('apis/drive/varlist/', {
        template_name: this.templatename,
        device_name: this.subdevice_name,
        var_list: this.value
      })
        .then(response => {
          _this.$Message.SuccessMessage(_this, response.data.message)
          _this.flushtabledata()
        })
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
    chooseStatus (enable) { // 改变驱动状态
      this.changestatus(enable)
    },
    changestatus (val) {
      var _this = this
      this.$axios.post('apis/drive/enable/', {
        enable: val,
        template_name: this.templatename,
        device_name: this.subdevice_name,
        drive_name: this.templateForm[0][1],
        drive_type: this.templateForm[1][1]
      })
        .then(response => {
          _this.$Message.SuccessMessage(_this, response.data.message)
          // console.log(response);
        })
    },
    flushtabledata () {
      this.tableloading = true
      this.$axios.get('apis/device/data', {
        params: {
          subdevice: this.subdevice_name,
          template_name: this.templatename,
          // template_name: JSON.parse(sessionStorage.getItem('template_'+this.subdevice_name)),
          row: 0
        }
      }) // 最近一条数据
        .then(response => {
          if (response.data.status_code == 1) {

          } else {
            this.tableData = response.data.tableData
            this.formatData = response.data.formatData
            this.Total = response.data.Total
            this.uri = response.data.URI
            this.data = response.data.key
          }
        })
      setTimeout(() => {
        this.tableloading = false
      }, 300)
    },
    flushtemplatedata () {
      this.loading = true
      var template = ''
      this.$axios.get('apis/device/apply', {
        params: {
          subdevice: this.subdevice_name
        }
      }) // 设备最新应用
        .then(response => {
          this.templateForm = response.data.db
          this.templatename = response.data.template_name
          // window.sessionStorage.setItem('template_'+this.subdevice_name, JSON.stringify(response.data.template_name));
          this.flushtabledata()
        })
      setTimeout(() => {
        this.loading = false
      }, 300)
    }
    // timer() {
    //   return setTimeout(()=>{
    //         this.flushtabledata()
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
</style>
