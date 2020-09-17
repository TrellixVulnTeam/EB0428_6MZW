<template>
  <el-main class="no-padding">
    <el-row  style=" padding-left: 10px">
      <el-col >
        <el-select size="small"  v-model="choose" placeholder="Choose Attribute">
            <el-option v-for="item in params" :key="item.index" :label="item.value" :value="item.value">
            </el-option>
        </el-select>
        <el-button type="primary" size="small" plain style="margin-left: 5px" @click="plot()">数据</el-button>
        <el-radio-group v-model="type" style="margin-left: 30px" size="small">
          <el-radio-button label="trend">趋势图</el-radio-button>
          <el-radio-button label="control">控制图</el-radio-button>
          <el-radio-button label="corr" >相关性</el-radio-button>
        </el-radio-group>

      </el-col>
  
    </el-row>
    <el-row  class="el-row-margin row-self" >    
       <!-- 模板接口信息 -->
      <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" style="width: 100%">
          <el-card 
            style="height: 600px"
            class="table-card" 
            shadow="hover" 
            size="small">
            <h4 class="title-style">Raw-Data 
            <!-- <el-button type="success" size="mini" icon="el-icon-refresh" @click="flushtemplatedata()" plain>刷新</el-button> -->
            </h4>
            <el-table :data="tableData" tooltip-effect="dark"  :row-key="getRowKeys" class="feature-card" style="width: 29%; float: left"  height="480">
              <el-table-column label="create_time" prop="create_time" style="width: 160px" ></el-table-column>
              <el-table-column label="value" prop="value" style="width: 110px "></el-table-column>

            </el-table>
            <div 
              v-loading="loading"
               shadow="hover" 
            >
            <img v-if='type === "trend"' :src='require("../../../"+img[0])' alt="" style="float: left; margin-left:10px" width="69%" height=420px>
            <img v-else-if='type === "control"' :src='require("../../../"+img[1])' alt="" style="float: left; margin-left:10px" width="69%" height=420px>
            <img v-else  :src='require("../../../"+img[2])' alt="" style="float: left; margin-left:10px" width="69%" height=420px>
           </div>
        </el-card>
      </el-col> 
                
    </el-row>
  
  </el-main>
</template>

<script>
import Clipboard from 'clipboard';
import { toUnicode } from 'punycode'

export default {

  data() {
    return {
      subdevice_name: JSON.parse(window.sessionStorage.getItem('subdevice')),
      img : ["assets/device/HC33AMeter_trend.png","assets/device/HC33AMeter_control.png", "assets/device/HC33AMeter_corr.png"],
      type: "control",
      loading: false,
      choose : '',
      params : [
          { index: 0, value: 'None'},
      ],
      tableData: [
        // {property: "Temperature",value: 28},
        // {property: "humidity",value: 40},
        // {property: "humidity",value: 40},
        // {property: "Temperature",value: 28},
      ],
      
    };
  },
  mounted() {
    
  },
  created() {
    this.flush_1();
  },
  methods: {
    getRowKeys(row){
        return row.property
      },
    plot() {
      this.loading = true;

      this.$axios.get("apis/device/plot", {
        params:{            
          subdevice: this.subdevice_name,
          param: this.choose
        }
      }) //设备最新应用
      .then(response => {
        console.log(response)
        this.img = response.data.img_list;
        this.tableData = response.data.db;
      })
      setTimeout(() =>{
          this.type = "trend";
          this.loading = false
      },300)
     
    },
    flush_1() {
      this.$axios.get("apis/device/status_img", {
        params:{            
          subdevice: this.subdevice_name
        }
      }) //设备最新应用
      .then(response => {
        console.log(response)
        // this.img = response.data.img;
        this.params = response.data.attribute;
      })
    } 
   
  },
  
};
</script>

<style >
.el-radio-button__orig-radio:checked+.el-radio-button__inner {
    color: #FFF;
    background-color: #08c78f;
    border-color: #08c78f;
    -webkit-box-shadow: -1px 0 0 0 #08c78f;
    box-shadow: -1px 0 0 0 #08c78f;
}
</style>
