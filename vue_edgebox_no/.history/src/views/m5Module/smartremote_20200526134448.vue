<template>
  <el-main class="no-padding smartremote">
    <!-- 面包屑 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>智能产品对接</el-breadcrumb-item>
      <el-breadcrumb-item>智能设备下发</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="smartrow">
    <el-row class="row-padding">
      <el-alert title="智能产品是本网关(Edge Box)的采集能力扩展模块,具有设备即插即用,数据快速转存等功能" type="success" show-icon></el-alert>
    </el-row>
    <el-row >
        <el-col :span="12">
          <el-card class="card" v-loading="card1">
            <div style="float: left;">
              <img v-if="card_data1[1][1] ==='NA'" src="../../assets/m5_b.png" class="image">
              <img v-else src="../../assets/m5.png" class="image">
              <div class="button" >
                  <el-button v-if="card_data1[1][1] === 'NA'" type="primary" disabled size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button v-else type="primary" @click="getRowInfo('01', card_data1[1][1])" size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button type="success" size="mini" icon="el-icon-refresh" @click="flush('01')" plain></el-button>
              </div> 
            </div>
            <div class="content" >
              <el-form  label-width="70px"  label-position="left" class="feature-card">
                <el-form-item v-for="(item ,index) of card_data1" :key="index" :label="item[0]">
                  <div v-if="item[0] === '啟用狀態' "> 
                    <el-tooltip v-if="card_data1[1][1] ==='NA'" content="通道未连接！"  placement="right-end">
                        <el-switch stype='width: 30px' disabled v-model="item[1]" @change="chooseStatus(item[1], '01')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                    <el-tooltip v-else content="点击启用关闭设备通道"  placement="right-end">
                        <el-switch stype='width: 30px' v-model="item[1]" @change="chooseStatus(item[1], '01')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                  </div>
                  <div v-else>
                    <span style='color: #999;'>{{item[1]}}</span>
                    
                  </div> 
                </el-form-item>
              </el-form>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12" >
            <el-card  class="card" v-loading="card2" >
            <div style="float: left">
              <img v-if="card_data2[1][1] ==='NA'" src="../../assets/m5_b.png" class="image">
              <img v-else src="../../assets/m5.png" class="image">
              <div  class="button" >
                  <el-button v-if="card_data2[1][1] === 'NA'" type="primary" disabled size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button v-else type="primary" @click="getRowInfo('02', card_data2[1][1])" size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button type="success" size="mini" icon="el-icon-refresh" @click="flush('02')" plain></el-button>
              </div> 
            </div>
            <div class="content" >
              <el-form  label-width="70px" style="left: 1px" label-position="left" class="feature-card">
                <el-form-item v-for="(item ,index) of card_data2" :key="index" :label="item[0]">
                  <div v-if="item[0] === '啟用狀態' "> 
                    <el-tooltip v-if="card_data2[1][1] ==='NA'" content="通道未连接！"  placement="right-end">
                        <el-switch stype='width: 30px' disabled v-model="item[1]" @change="chooseStatus(item[1],'02')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                    <el-tooltip v-else content="点击启用关闭设备通道"  placement="right-end">
                        <el-switch stype='width: 30px' v-model="item[1]" @change="chooseStatus(item[1],'02')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                  </div>
                  <div v-else>
                    <span style='color: #999;'>{{item[1]}}</span>
                    
                  </div> 
                </el-form-item>
              </el-form>
            </div>
            </el-card>
        </el-col>
    </el-row>
    <!-- <div style="padding: 20px"></div> -->
    <el-row>
         <el-col :span="12" >
            <el-card class="card" v-loading="card3">
            <div style="float: left">
              
              <img v-if="card_data3[1][1] ==='NA'" src="../../assets/m5_b.png" class="image">
              <img v-else src="../../assets/m5.png" class="image">
              <div class="button" >
                  <el-button v-if="card_data3[1][1] === 'NA'" type="primary" disabled size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button v-else type="primary" @click="getRowInfo('03',card_data3[1][1])" size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button type="success" size="mini" icon="el-icon-refresh" @click="flush('03')" plain></el-button>
              </div> 
            </div>
            <div class="content">
              <el-form  label-width="70px" style="left: 1px;" label-position="left" class="feature-card">
                <el-form-item v-for="(item ,index) of card_data3" :key="index" :label="item[0]">
                  <div v-if="item[0] === '啟用狀態' "> 
                   <el-tooltip v-if="card_data3[1][1] ==='NA'" content="通道未连接！"  placement="right-end">
                        <el-switch stype='width: 30px' disabled v-model="item[1]" @change="chooseStatus(item[1], '03')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                    <el-tooltip v-else content="点击启用关闭设备通道"  placement="right-end">
                        <el-switch stype='width: 30px' v-model="item[1]" @change="chooseStatus(item[1], '03')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                  </div>
                  <div v-else>
                    <span style='color: #999;'>{{item[1]}}</span>
                  </div> 
                </el-form-item>
              </el-form>
            </div>
            </el-card>
        </el-col>
        <el-col :span="12"  >
            <el-card class="card" v-loading="card4" >
            <div style="float: left">
              <img v-if="card_data4[1][1] ==='NA'" src="../../assets/m5_b.png" class="image" >
              <img v-else src="../../assets/m5.png" class="image">
              <div class="button" >
                  <el-button v-if="card_data4[1][1] === 'NA'" type="primary" disabled size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button v-else type="primary" @click="getRowInfo('04', card_data4[1][1])" size = 'mini' style="padding: 10px;" plain>数据管理</el-button>
                  <el-button type="success" size="mini" icon="el-icon-refresh"  @click="flush('04')" plain></el-button>
              </div>   
            </div>
            <div class="content">
              <el-form  label-width="70px" style="left: 1px" label-position="left" class="feature-card">
                <el-form-item v-for="(item ,index) of card_data4" :key="index" :label="item[0]">
                  <div v-if="item[0] === '啟用狀態' "> 
                    <el-tooltip v-if="card_data4[1][1] ==='NA'" content="通道未连接！"  placement="right-end">
                        <el-switch stype='width: 30px' disabled v-model="item[1]" @change="chooseStatus(item[1], '04')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                    <el-tooltip v-else content="点击启用关闭设备通道"  placement="right-end">
                        <el-switch stype='width: 30px' v-model="item[1]" @change="chooseStatus(item[1], '04')" 
                          active-color="#409eff" 
                          inactive-color="#DCDFE6">
                        </el-switch>
                    </el-tooltip>
                  </div>
                  <div v-else>
                    <span style='color: #999;'>{{item[1]}}</span>
                  </div> 
                </el-form-item>
              </el-form>
            </div>
            </el-card>
        </el-col>
    </el-row>
    </div>
    
  </el-main>
</template>

<script>
import { toUnicode } from 'punycode'
export default {
    data() {
        return {
          card1: false,
          card2: false,
          card3: false,
          card4: false,

          card_data1:[
            ['通道名稱', "01"],
            ['設備名稱', "NA"],
            ['啟用狀態', false],
            ['In/Out', "NA"],
            ['採集描述', 'NA'],
           ],
           card_data2:[
            ['通道名稱', "02"],
            ['設備名稱', "NA"],
            ['啟用狀態', false],
            ['In/Out', "NA"],
            ['採集描述', 'NA'],
           ],
           card_data3:[
            ['通道名稱', "03"],
            ['設備名稱', "NA"],
            ['啟用狀態', false],
            ['In/Out', "NA"],
            ['採集描述', 'NA'],
           ],
           card_data4:[
            ['通道名稱', "04"],
            ['設備名稱', "NA"],
            ['啟用狀態', false],
            ['In/Out', "NA"],
            ['採集描述', 'NA'],
           ],
        }
    },
    created() {
        this.flush("01");
        this.flush("02");
        this.flush("03");
        this.flush("04");
    },
    methods: {
      chooseStatus(status, pip_no){
        console.log(status);
        var _this = this;
        this.$axios.post('apis/m5/pip_enable/', {
            pip_no: pip_no,
            enable: status
          })
          .then(function (response) {
            _this.$Message.SuccessMessage(_this, response.data.message);
            _this.getData(pip_no)
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      getData(pipe_no) {
        this.$axios.get("apis/m5/pipe/", {
          params:{
            pipe_no: pipe_no,
          }
        }) // 最近一条数据
        .then(response => {
          if(response.data.status_code === 1){
            this.$Message.ErrorMessage(this, response.data.error);
          }
          else{
            switch(pipe_no){
              case "01":
                this.card_data1 = response.data.varlist;
                break;
              case "02":
                this.card_data2 = response.data.varlist;
                break;
              case "03":
                this.card_data3 = response.data.varlist;
                break;
              case "04":
                this.card_data4 = response.data.varlist;
                break;
                
            }
            // this.card_data1[0][1] = response.data.varlist.pipe_name;
            // this.card_data1[1][1] = response.data.varlist.pipe_device_name;
            // this.card_data1[2][1] = response.data.varlist.pipe_device_enable;
            // this.card_data1[3][1] = response.data.varlist.pipe_in_out;
            // this.card_data1[4][1] = response.data.varlist.pipe_remark;
          }
        } )
      },
      flush(index) {
        switch(index){
          case "01":
            this.card1 = true
            this.getData("01");
            setTimeout(() =>{
              this.card1 = false
            },300)
            break
          case "02":
            this.card2 = true
            this.getData("02");
            setTimeout(() =>{
              this.card2 = false
            },300)
            break
          case "03":
            this.card3 = true
            this.getData("03");
            setTimeout(() =>{
              this.card3 = false
            },300)
            break
          case "04":
            this.card4 = true
            this.getData("04");
            setTimeout(() =>{
              this.card4 = false
            },300)
            break
        }
        
      },
      getRowInfo(index, subdevice) {
        window.sessionStorage.setItem('pip_index', JSON.stringify(index));
        window.sessionStorage.setItem('subdevice', JSON.stringify("m5_"+index+"_"+subdevice));
        this.$router.push({path: 'deviceManage', query:{ subdevice : subdevice}});
      },

   }
}

</script>

<style >

.smartrow .content {
  float: left;
  padding: 0px 30px 6px 10px;
}

.smartrow .image {
  width: 150px;
  height: 150px;
}

.smartrow .button {
  padding: 0px 10px;
}

.smartrow .card {
  height: 250px;
}

.smartrow .text {
    font-size: 11px;
  }

.smartrow .item {
  margin-bottom: 18px;
}
</style>