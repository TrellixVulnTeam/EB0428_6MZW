<template>
  <div class="block">
    <el-alert
    title="提示: 只能上传.py/.pyc文件，模型参数输入输出格式请参考模板文件"
    type="warning"
    show-icon>
    </el-alert>
    <el-row  class="el-row-margin row-self" >   
        <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" style="width: 30%; margin-top:10px; height:400px">
        <el-upload
            class="upload-demo"
            ref="upload"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选择模型文件</el-button>
            <el-button size="small" style="margin-left: 10px; margin-bottom:10px" type="primary">设备模型库</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">更新保存</el-button>
        </el-upload>
        </el-col>
        <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12" style="width: 66%; margin-top:10px; height:400px">

        </el-col>
    </el-row>
  </div>
</template>

<script>
import { checkNull } from '../../../until/checkRules.js'
export default {
  data() {
    return {
      subdevice_name: JSON.parse(window.sessionStorage.getItem('subdevice')),
      loading: false,
      fileList: [{
         name: '模型示例.pyc',
         url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'},
        ],
       tableData3: []
    };
  },
  created() {
    // this.flushtabledata();
  },
  mounted() {
  },
  methods: {
    submitUpload() {
    this.$refs.upload.submit();
    },
    handleRemove(file, fileList) {
    console.log(file, fileList);
    },
    handlePreview(file) {
    console.log(file);
    }
    }
  }
</script>

<style >
.el-timeline-item__node {
    background-color: #08c78f;
}
</style>