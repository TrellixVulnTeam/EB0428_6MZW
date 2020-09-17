<template>
  <div class="block">
    <el-form
        style=" padding-left:10px"
        :inline="true"
        :model="timeForm"
        ref="timeForm"
        :rules="timeRules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item >
          <el-date-picker
            v-model="timeForm.queryTime"
            size="small"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small" @click="getLogbytime()" >查询</el-button>
        </el-form-item>
    </el-form>
    <el-card 
        v-loading="loading"
        style=" margin-top:0px"
        class="table-card" 
        shadow="hover" 
        size="small">
        <el-timeline>
          <el-timeline-item
            v-for="(activity, index) in activities"
            :key="index"
            :timestamp="activity.timestamp"
          >
          <span v-if="index===0" style="color:#08c78f">{{activity.content}}</span>
          <span v-else  :sub="index">{{activity.content}}</span>
          </el-timeline-item>
        </el-timeline>
    </el-card>
  </div>
</template>

<script>
import { checkNull } from '../../../until/checkRules.js'
export default {
  data() {
    return {
      subdevice_name: JSON.parse(window.sessionStorage.getItem('subdevice')),
      loading: false,
      activities: [
        {
          content: "17:30:32 设备 <XXXX> 应用了*#####*模板  ",
          timestamp: "2019-06-21"
        },
      ],
      pickerOptions: {
          shortcuts: [{
            text: '最近一小时',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 1);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一天',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }]
      },
      timeForm: {
          queryTime: ''
      },
      
      timeRules: {
          queryTime: [
              {
                  required: false, validator: checkNull, trigger: 'change'
              }
          ]
      }
    };
  },
  created() {
    this.getLog();
    // this.flushtabledata();
  },
  methods: {
    getLog() {
        this.loading = true;
        this.$axios.get("apis/log/list/", {
          params:{
            device_name: this.subdevice_name,
          }
        }) // 最近6条数据
        .then(response => {
          if(response.data.status_code === 1){
            this.$Message.ErrorMessage(this, response.data.error);
          }
          else{
            this.activities = response.data.db;
          }
        } )
        setTimeout(() =>{
        this.loading = false
        },300)
    },
    getLogbytime() {
        if(this.timeForm.queryTime === ""){
          //  this.$Message.ErrorMessage(this, "请先选择时间段,再进行查找");
        }
        else{
          this.loading = true;
          this.$axios.get("apis/log/select/", {
            params:{
              device_name: this.subdevice_name,
              start: this.timeForm.queryTime[0].valueOf(),
              end: this.timeForm.queryTime[1].valueOf(),
            }
          }) 
          .then(response => {
            if(response.data.status_code === 1){
              this.$Message.ErrorMessage(this, response.data.error);
            }
            else{
              this.activities = response.data.db;
            }
          } )
          setTimeout(() =>{
            this.loading = false
            },300)
        }
        
        
    },
  }
};
</script>

<style >
.el-timeline-item__node {
    background-color: #08c78f;
}
</style>>