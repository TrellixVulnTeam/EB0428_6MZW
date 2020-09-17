<!-- 应用模板弹出框 -->
<template>
    <div>
     <el-tabs v-model="activeName" :tab-position="tabPosition" @tab-click="handleClick" style="height: 50%;">
        <el-tab-pane label="Data" name="Data">
            <el-input :value="data_"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 12}">
            </el-input>
            <!-- <textarea v-model="data_ac" placeholder="多行文本"></textarea>      -->

        </el-tab-pane>
        <el-tab-pane label="Plot" name="Plot">
             <div style="margin-top: 0px">
                <el-radio-group v-model="radio" size="mini" @change="changevar()" >
                    <el-radio-button  v-for="(item ,index) of radio_list" :key="index" :label="item" ></el-radio-button>
                </el-radio-group>
            </div>
            <div ref="plot" style="width: 750px; height: 300px">
            </div>
        </el-tab-pane>
     </el-tabs>
      <el-row  slot="footer">
        <el-input-number v-model="number" controls-position="right"
         @change="handleChange"  :step="1000" :min="1000" :max="total"
         style="margin-top: 10px"></el-input-number>
        <!-- <el-button type="primary" size="small" @click="applyForm('form')">应用</el-button> -->
        <!-- <el-button type="default" size="small" @click="resetForm('form')">重置</el-button> -->
        <!-- <el-button type="default" size="small" @click="close">重置</el-button> -->

      </el-row>
    </div>
</template>


<script>

export default {
    props: ["fileName", 'subdevice_name', 'templatename'],
    data() {
       return {
        tabPosition:"top",
        activeName: 'Plot',
        number: 1000,
        data: [],
        data_: "123456",
        radio: "ax",
        radio_list: ["ax"],
        values: [],
        data_index: [],
        total: 10000,
        Hex: ["feefds", "fdsfdf", "fdfsdf", "323dsd"],
        Ac: ["feefds", "fdsfdf", "fdfsdf", "323dsd"],
        Plot: ["feefds", "fdsfdf", "fdfsdf", "323dsd"]

       }
    },
    created() {
       if(this.fileName=="Live charts"){
         console.log(this.fileName)
         this.getData()
       }else{
         this.getfileNameData();
       }
      this.positionTimer = setInterval(() => {
        this.changevar()
      }, 500)
        // console.log(this.data_ac)
    },
    mounted(){
    //    this.dataconvert();
    //    this.$nextTick(() => {
    //         this.echart();
    //       });
    },
    destroyed () {
        clearInterval(this.positionTimer)// 清除定时器
        this.positionTimer = null
    // console.log('关闭定时器')
    },
    methods: {
  
      changevar(){
        console.log(this.radio);
        this.$axios.get("apis/device/dbdata/", {
        params:{
            subdevice_name: this.subdevice_name,
            templatename: this.templatename,
            param: this.radio
        }
        }) 
        .then(response => {
        if(response.data.status_code === 1){
            this.$Message.ErrorMessage(this, response.data.error);
        }
        else{
            this.radio_list = response.data.params
            this.data_index = response.data.data_index;

            this.values = response.data.value
            this.dataconvert2(this.values);
            this.$nextTick(() => {
                    this.echart();
                });
        }
        } )

      },
      handleChange(value) {
        console.log(value);
      },
      getData(){
           // 获取磁盘数据
        this.$axios.get("apis/device/dbdata/", {
            params:{
                subdevice_name: this.subdevice_name,
                templatename: this.templatename
            }
            }) 
            .then(response => {
            if(response.data.status_code === 1){
                this.$Message.ErrorMessage(this, response.data.error);
            }
            else{
                this.radio_list = response.data.params
                // this.data_=response.data.data_db;
                this.data_index = response.data.data_index;

                this.radio = this.radio_list[0];
            
                this.values = response.data.value
                this.dataconvert2(this.values);
                this.$nextTick(() => {
                        this.echart();
                    });
            }
            } )

      },
      getfileNameData(){
           // 获取磁盘数据
        this.$axios.get("apis/device/filedata/", {
            params:{
                fileName: this.fileName,
            }
            }) 
            .then(response => {
            if(response.data.status_code === 1){
                this.$Message.ErrorMessage(this, response.data.error);
            }
            else{
                this.data = response.data.data_ac;
                this.data_index = response.data.data_index;
                this.dataconvert();
                this.$nextTick(() => {
                        this.echart();
                    });
            }
            } )

      },
      // 切换标签页时执行的方法
      handleClick(tab, event) {
        if (this.activeName === 'Plot') {
          this.$nextTick(() => {
            this.echart();
          });
          
        }
      },
      dataconvert2(values) {
          this.data_ = values.slice(0, 5000).join("\n")
      },
      dataconvert() {
          this.data_ = this.data.slice(0, 5000).join("\n")
      },

      echart() {
        let Myechart = this.$echarts.init(this.$refs.plot); // 获取dom节点
        // var timeData = [];
             
        // var timeData = this.data;
        var timeData = this.values;

             
        var timeseries = this.data_index;

        var id=Math.round(Math.random()); 
        // var id=Math.floor(Math.random()*3);
        var color = ['#08c79b', '#3a8ee6'];

        // 折线图选项
      
        let option_line = {
                  // Make gradient line here
            // visualMap: [
            //     {
            //     show: false,
            //     type: 'continuous',
            //     seriesIndex: 0,
            //     dimension: 0,
            //     min: 0,
            //     max: timeseries.length
            // }],

            color: color[0],
            title: [{
                left: 'center',
                // text: 'Sample',
                // subtext: 'AC Value',
            }],
            tooltip: {
                trigger: 'axis'
            },
            xAxis: [{
                data: timeseries
            }, ],
            yAxis: [{
                splitLine: {show: false}
            }, ],
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    animation: false
                }
            },
            dataZoom: [
            {
                // show: true,
                realtime: false,
                start: 0,
                end: 100,
                // xAxisIndex: [0, 1]
            },
            {
                type: 'inside',
                realtime: false,
                start: 0,
                end: 100,
                // xAxisIndex: [0, 1]
            }
            ],
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            series: [{
                type: 'line',
                showSymbol: false,
                data: timeData
            }]
            };

            Myechart.setOption(option_line);
            },
            }
        }
</script>

<style >
.dialog-form .el-dialog__body {
    padding: 0px 20px 15px 20px;
}
</style>
    