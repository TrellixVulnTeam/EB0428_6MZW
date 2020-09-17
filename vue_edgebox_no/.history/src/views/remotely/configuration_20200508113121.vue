<template>
  <el-main class="no-padding">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>远程管理及维护</el-breadcrumb-item>
      <el-breadcrumb-item>配置下发</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-small-padding">
      <el-alert title="该功能实现远程对网关的配置下发！目前只支持MQTT接口" type="info" show-icon></el-alert>
    </el-row>
    <el-tooltip :content="'配置下发通道开关'" placement="top">
      <el-switch
        v-model="is_active"
        active-text = "打开配置下发接口"
        inactive-text = "关闭配置下发接口"
        active-color="#13ce66"
        inactive-color="#ff4949"
        @change="changestatus()"
        >
      </el-switch>
    </el-tooltip>
    <el-table :data="tableData" v-loading="loading" windh="100%">
      <el-table-column label="下发类型" prop="down_type" min-width="14%"></el-table-column>
      <el-table-column label="Topic主题"  min-width="37%">
        <template v-slot="scope">
          <span>{{scope.row.down_topic}}</span>&nbsp;
          <el-button type="text" class="el-icon-document tag-read" @click="paste(scope.row.down_topic)"></el-button>
        </template>
      </el-table-column>
      <el-table-column sortable label="成功" prop="down_num" min-width="7%">
          <template slot-scope="scope">
            <el-tag size="medium" style="border-bottom: solid;">{{ scope.row.down_num }}</el-tag>
          </template>
      </el-table-column>
      <el-table-column sortable label="失败" prop="down_num2" min-width="7%">
          <template slot-scope="scope">
            <el-tag size="medium" type="warning" style="border-bottom: solid;">{{ scope.row.down_num2 }}</el-tag>
          </template>
      </el-table-column>
      <el-table-column label="描述" prop="down_remark"  min-width="24%"></el-table-column>
      <el-table-column label="操作" min-width="10%">
        <template v-slot="scope">
          <el-button type="text" size="small" @click="openDraw(scope.row.down_topic,scope.row.down_type)">使用说明</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-drawer
      title="MQTT连接说明"
      :show-close="isclose"
      :visible.sync="drawer"
      :direction="direction"

      size="50%">
      <div style="position:relative;overflow:auto;width:100%;border: 1px solid #ccc;max-height:100%">

      <el-table style="padding-left:20px" :data="table_data">
        <el-table-column label="Host" prop="host"></el-table-column>
        <el-table-column label="Port" prop="port"></el-table-column>
        <el-table-column label="Username" prop="user"></el-table-column>
        <el-table-column label="Password" prop="pass"></el-table-column>
      </el-table>
      <el-table style="padding-left:20px" :data="table_data">
        <el-table-column label="功能" prop="type" min-width="25%"></el-table-column>
        <el-table-column label="主題" prop="topic" min-width="60%"></el-table-column>
      </el-table>
      <!-- <el-divider></el-divider> -->
      <span class="el-drawer__header" style="color:#72767b;padding-top:10px;">上传消息格式</span>
      <!-- <pre style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
        {
           <span style="color:#FF0000">"func_name":</span> <span style="color:#009933">"create_update_device",</span>
           <span style="color:#FF0000">"param":</span> {
              <span style="color:#FF0000">"subdevice_type":</span> <span style="color:#009933">"新增设备所属类别",</span>
              <span style="color:#FF0000">"subdevice_name":</span> <span style="color:#009933">"新增设备名称",</span>
              <span style="color:#FF0000">"subdevice_model":</span> <span style="color:#009933">"新增设备型号",</span>
              <span style="color:#FF0000">"subdevice_position":</span> <span style="color:#009933">"新增设备位置:",</span>
              <span style="color:#FF0000">"subdevice_remark":</span> <span style="color:#009933">"新增设备相关描述",</span>
            }
        }
      </pre> -->
      <el-form :data="tableData" style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
         <el-form-item>
            <json-viewer
              :value="statusInfos"
              :expand-depth="5"
              copyable
              boxed
              sort
            ></json-viewer>
        </el-form-item>
      </el-form>
      <span class="el-drawer__header" style="color:#72767b;padding-top:0px;">状态返回格式</span>
      <pre style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
        {
          <span style="color:#FF0000">"status_code":</span> <span style="color:#009933">200/400 ,</span>
          <span style="color:#FF0000">"message":</span> <span style="color:#009933">Success/Fail</span>
        }
      </pre>
      </div>
    </el-drawer>
  </el-main>
</template>

<script>
import Clipboard from 'clipboard'
export default {
  data () {
    return {
      is_active: false,
      isclose: false,
      drawer: false,
      loading: false,
      // positionTimer:
      direction: 'rtl',
      table_data: [{
        topic: '',
        type: '',
        user: 'iot',
        pass: 'iot123!',
        host: '127.0.0.1',
        port: '1883'
      }],
      tableData: [],
      statusInfos:{},
    }
  },
  created(){
    this.getData()
    // 这是一个定时器
    this.positionTimer = setInterval(() => {
      this.getData()
    }, 3000)
  },
  destroyed () {
    clearInterval(this.positionTimer)// 清除定时器
    this.positionTimer = null
    // console.log('关闭定时器')
  },
  methods: {
    getData() {
      this.$axios.get('/apis/remotely/list/')
      .then(response => {
        this.tableData = response.data.db
        this.is_active = response.data.enable
        this.statusInfos = response.data
        this.loading = false
        // if(this.is_active){
        //   // 这是一个定时器
        //   this.positionTimer = setInterval(() => {
        //     this.getData()
        //   }, 3000)
        // }
      })
      .catch(error => {
        console.log(error)
      })
    },
    // 复制tpoic
    paste (topic) {
      let clipboard = new Clipboard('.tag-read', {
        text: function () {
          return topic
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
    changestatus() {
      var _this = this 
      this.$axios.post("apis/remotely/setting/enable/", {
            enable: _this.is_active,
          }) 
        .then(response => {
          if(response.data.status_code==1){
            _this.$Message.ErrorMessage(_this, response.data.message);
          }
          else{
            _this.$Message.SuccessMessage(_this, response.data.message);
          }

        })
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    openDraw(topic,type){
      this.table_data[0].topic = topic
      this.table_data[0].type = type
      this.drawer = true
    },
    status(row) {
      // this.drawer = true
      // this.$axios.get("apis/device/path/info",{
      //     params:{            
      //           subdevice: this.subdevice_name,
      //           path_name: row.addressName,
      //           path_type: row.type
      //         }
      // }) //设备协议清单
      // .then(response => {
      //   this.statusInfo = response.data.status;
      //   this.subInfo = response.data.sub
      // })

    }
  }
}
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0;
}
.el-drawer__header {
  margin-bottom: 10px;
}
</style>
