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
    <span v-if="is_active==false">
      <el-tooltip content="开启配置下发" placement="top">
        <el-button type="success" size="small" @click="is_active">开启</el-button>
      </el-tooltip>

    </span>
    <span v-else>
      <el-tooltip content="关闭配置下发" placement="top">
        <el-button type="success" size="small" @click="is_active">关闭</el-button>
      </el-tooltip>

    </span>
    <!-- <el-tooltip :content="'配置下发通道开关'" placement="top">
      <el-switch
        v-model="is_active"
        active-text = "打开配置下发接口"
        inactive-text = "关闭配置下发接口"
        active-color="#13ce66"
        inactive-color="#ff4949"
        @change="changestatus()"
        >
      </el-switch>
    </el-tooltip> -->
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
          <el-button type="text" size="small" @click="openDraw(scope.row)">使用说明</el-button>
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

      <el-table style="padding-left:20px" :data="mqtt_data">
        <el-table-column label="Host" prop="host"></el-table-column>
        <el-table-column label="Port" prop="port"></el-table-column>
        <el-table-column label="Username" prop="user"></el-table-column>
        <el-table-column label="Password" prop="pass"></el-table-column>
      </el-table>
      <el-table style="padding-left:20px" :data="table_data">
        <el-table-column label="功能" prop="down_type" min-width="25%"></el-table-column>
        <el-table-column label="主題" prop="down_topic" min-width="60%"></el-table-column>
      </el-table>

      <span class="el-drawer__header" style="color:#72767b;padding-top:10px;">上传消息格式示例</span>

      <el-form style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
         <el-form-item>
            <json-viewer
              :value="table_data[0].down_param"
              :expand-depth="5"
              copyable
              sort
            ></json-viewer>
        </el-form-item>
      </el-form>
      <span class="el-drawer__header" style="color:#72767b;padding-top:0px;">状态返回格式</span>

      <el-form style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
        <el-form-item>
            <json-viewer
              :value="statusInfoss"
              :expand-depth="5"
              sort
            ></json-viewer>
        </el-form-item>
      </el-form>
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
      mqtt_data: [{
        user: 'iot',
        pass: 'iot123!',
        host: '127.0.0.1',
        port: '1883'
      }],
      tableData: [],
      statusInfoss:{"status_code":"200/400", "message":"Success/Fail"},
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
    openDraw(row){
      // this.table_data[0].topic = row.topic
      // this.table_data[0].type = row.type
      this.table_data = [row]
      this.drawer = true
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
