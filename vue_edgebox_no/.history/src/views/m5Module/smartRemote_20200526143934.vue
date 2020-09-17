<template>
  <el-main class="no-padding smartremote">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>智能产品对接</el-breadcrumb-item>
      <el-breadcrumb-item>智能设备管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row class="row-padding">
      <el-alert title="智能设备扩展模块的远程配置下发" type="success" show-icon></el-alert>
    </el-row>
    <el-collapse accordion value="1">
      <el-collapse-item name="1">
        <template slot="title">
          硬件扫描任务 <i class="header-icon el-icon-view"></i>
        </template>
        <el-form ref="form" :model="sizeForm" label-width="100px" size="mini">
          <el-form-item label="任务启用">
            <el-radio-group v-model="sizeForm.type">
              <el-radio-button label="Auto" >自 动</el-radio-button>
              <el-radio-button label="Manual" >手 动</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item  label="任务状态">
            <el-select v-if='sizeForm.type === "Auto"' disabled  v-model="sizeForm.status" placeholder="驱动状态">
              <!-- <el-option label="启动" value="Run"></el-option>
              <el-option label="停止" value="Stop"></el-option> -->
            </el-select>
            <el-select v-if='sizeForm.type === "Manual"'  v-model="sizeForm.status" placeholder="驱动状态">
              <el-option label="启动" value="Run"></el-option>
              <el-option label="停止" value="Stop"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="扫描类型">
            <el-select v-model="sizeForm.scanftype" placeholder="扫描类型">
              <el-option label="USB接口/COM口" value="COM"></el-option>
              <el-option label="Ethernet-有线"  disabled value="NET"></el-option>
              <el-option label="WiFi-无线"  disabled value="WiFi"></el-option>

            </el-select>
          </el-form-item>
          <el-form-item label="设备连接数">
            <el-input-number v-model="sizeForm.Number" @change="handleChange" :min="1" :max="4" ></el-input-number>
          </el-form-item>
          <el-form-item size="small">
            <el-button>恢复默认设置</el-button>
            <el-button type="success" >立即生效</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item>
      <el-collapse-item name="2">
        <template slot="title">
         设备数据缓存 <i class="el-icon-tickets"></i>
        </template>
        <el-form ref="form" :model="databases" label-width="100px" size="mini">
          <el-form-item label="数据库">
            <el-select v-model="databases.type" placeholder="扫描类型">
              <el-option label="Sqlite" value="sqlite"></el-option>
              <el-option label="MySQL"  disabled value="mysql"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="缓存设置">
            <el-radio-group v-model="databases.setting">
              <el-radio-button label="size" >大 小</el-radio-button>
              <el-radio-button label="day" >天 数</el-radio-button>
            </el-radio-group>
            <el-select style="margin-left: 10px" v-if='databases.setting === "size"' v-model="databases.size"   placeholder="M">
              <el-option v-for="item in databases.sizeList" :disabled="item.disabled" :key="item.index" :label="item.index" :value="item.index">
                 <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
              </el-option>
            </el-select>
            <el-select style="margin-left: 10px" v-if='databases.setting === "day"' v-model="databases.day"  placeholder="day">
              <el-option v-for="item in databases.dayList" :disabled="item.disabled" :key="item.index" :label="item.index" :value="item.index">
                 <span style="float: left; font-size: 12px ">{{ item.index }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ item.value }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item size="small">
            <el-button>恢复默认设置</el-button>
            <el-button type="success" >立即生效</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item>
      <!-- <el-collapse-item name="3">
        <template slot="title">
          数据转发引擎 <i class="el-icon-upload"></i>
        </template>
        <el-form ref="form" :model="sizeForm" label-width="100px" size="mini">
          <el-form-item label="任务启用">
            <el-radio-group v-model="sizeForm.type">
              <el-radio-button label="Auto" >自 动</el-radio-button>
              <el-radio-button label="Manual" >手 动</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item  label="任务状态">
            <el-select v-if='sizeForm.type === "Auto"' disabled  v-model="sizeForm.status" placeholder="驱动状态">
          
            </el-select>
            <el-select v-if='sizeForm.type === "Manual"'  v-model="sizeForm.status" placeholder="驱动状态">
              <el-option label="启动" value="Run"></el-option>
              <el-option label="停止" value="Stop"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="扫描类型">
            <el-select v-model="sizeForm.scanftype" placeholder="扫描类型">
              <el-option label="USB接口/COM口" value="COM"></el-option>
              <el-option label="Ethernet-有线"  disabled value="NET"></el-option>
              <el-option label="WiFi-无线"  disabled value="WiFi"></el-option>

            </el-select>
          </el-form-item>
          <el-form-item label="设备连接数">
            <el-input-number v-model="sizeForm.Number" @change="handleChange" :min="1" :max="4" ></el-input-number>
          </el-form-item>
          <el-form-item size="small">
            <el-button>恢复默认设置</el-button>
            <el-button type="success" >立即生效</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item> -->
    
  </el-collapse>

  </el-main>
</template>

<script>
export default {
    data() {
        return {
          databases:{
            type: "sqlite",
            setting: "size",
            size:"",
            day:"",
            sizeList: [
              {
                index: 100,
                value: "M",
                disabled: false
              },
              {
                index: 200,
                value: "M",
                disabled: false
              }
            ],
            dayList: [
              {
                index: 1,
                value: "day",
                disabled: false
              },
              {
                index: 3,
                value: "day",
                disabled: false
              }
            ],
            
          },
          sizeForm: {
            name: '',
            status: 'Run',
            date1: '',
            date2: '',
            delivery: false,
            type: "Auto",
            resource: '',
            scanftype: 'COM',
            Number: ''
          }
        }
    },
    created() {
        // this.$axios.get("apis/device/template") //设备协议清单
        // .then(response => {
        //     this.tableData = response.data.db;
        // })
    },
    methods: {
     

   }
}

</script>

<style >
.smartSetting .el-collapse-item__header {
  background-color: #409eff1c;
  color: #053044f5;
  padding: 0px 0px 0px 20px;
}
.smartSetting .el-icon-view:before{
  padding: 10px
}
.smartSetting .el-icon-tickets:before{
  padding: 10px
}
.smartSetting .el-icon-upload:before{
  padding: 10px
}
.smartSetting .el-collapse-item__content {
    padding-top: 20px;
    padding-left: 20px;
}
</style>