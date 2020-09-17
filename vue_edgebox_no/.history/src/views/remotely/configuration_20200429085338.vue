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
    <el-table :data="tableData" v-loading="loading" windh="100%">
      <el-table-column label="下发类型" prop="down_type" min-width="15%"></el-table-column>
      <el-table-column label="Topic主题"  min-width="35%">
        <template v-slot="scope">
          <span>{{scope.row.down_topic}}</span>&nbsp;
          <el-button type="text" class="el-icon-document tag-read" @click="paste(scope.row.down_topic)"></el-button>
        </template>
      </el-table-column>
      <el-table-column label="下发次数" prop="down_num"  min-width="15%"></el-table-column>
      <el-table-column label="描述" prop="down_remark"  min-width="25%"></el-table-column>
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
        <el-table-column label="数据类型" prop="type"></el-table-column>
        <el-table-column label="用户名" prop="user"></el-table-column>
        <el-table-column label="密码" prop="pass"></el-table-column>
      </el-table>
      <el-table style="padding-left:20px" :data="table_data">
        <el-table-column label="Topic" prop="topic"></el-table-column>
        <el-table-column label="Host" prop="host"></el-table-column>
        <el-table-column label="Port" prop="port"></el-table-column>
      </el-table>
      <el-divider></el-divider>
      <span class="el-drawer__header" style="color:#72767b;padding-top:0px;">上传消息格式说明</span>
      <pre style="position:relative;left:5%;width: 90%;border: 1px solid #ccc;text-align: left;outline: none">
{
  <span style="color:#FF0000">"create_params":</span> [
    {
      <span style="color:#FF0000">"subdevice_type":</span> <span style="color:#009933">"新增设备所属类别",</span>
      <span style="color:#FF0000">"subdevice_name":</span> <span style="color:#009933">"新增设备名称",</span>
      <span style="color:#FF0000">"subdevice_model":</span> <span style="color:#009933">"新增设备型号",</span>
      <span style="color:#FF0000">"subdevice_position":</span> <span style="color:#009933">"新增设备位置:",</span>
      <span style="color:#FF0000">"subdevice_remark":</span> <span style="color:#009933">"新增设备相关描述",</span>
    }
  ]
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
      isclose: false,
      drawer: false,
      loading: false,
      direction: 'rtl',
      table_data: [{
        topic: '',
        type: '',
        user: 'io',
        pass: 'iot123!',
        host: '10.129.7.199',
        port: '1883'
      }],
      tableData: []
    }
  },
  created(){
    this.$axios.get('/apis/remotely/list/')
      .then(response => {
        this.tableData = response.data.db
        this.loading = false
      })
      .catch(error => {
        console.log(error)
      })
  },
  methods: {
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
    }
  }
}
</script>

<style scoped>
.row-small-padding {
  margin: 10px 0;
}

</style>
