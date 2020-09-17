<template>
  <el-main class="no-padding">
      <el-form
        :inline="true"
        :model="timeForm"
        ref="timeForm"
        :rules="timeRules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item label="选择查询时间:">
          <el-date-picker
            v-model="timeForm.queryTime"
            size="small"
            type="datetimerange"
            format="yyyy-MM-dd HH:mm:ss"
            value-format="yyyy-MM-dd HH:mm:ss"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" size="small" @click="select()">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tableData">
        <template ></template>
          <el-table-column label="时间" prop="create_time" sortable>

          </el-table-column>
          <el-table-column label="文件名" prop="log_type" sortable>

          </el-table-column>
          <el-table-column label="管理者" prop="log_leader" sortable>

          </el-table-column>
          <el-table-column label="日志级别" prop="log_level" sortable>

          </el-table-column>
          <el-table-column label="描述" prop="log_info" sortable>

          </el-table-column>
      </el-table>

      <div class="block row-padding-top" style="float:right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="1"
          :page-sizes="[10,20,30,40,50,60,70,80,90,100]"
          :page-size="10"
          layout="total, sizes, prev, pager, next, jumper"
          :total=count>
        </el-pagination>
      </div>
  </el-main>
</template>

<script>
import { checkNull } from '../../../until/checkRules.js'
export default {
  data () {
    return {
      page: 1, // 当前页
      count: 1, // 记录
      size: 10, // 每页条数
      url: '/apis/loginfo/edgebox/?type=',
      starttime: null,
      endtime: null,
      tableData: [],
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
    }
  },
  props: {
    log_type: { // type 日志类型  (1, "系统日志"),(2, "采集日志"),(3, "传输日志"),(4, "网络日志"),(5, "权限日志")
      type: Number,
      required: true,
      default: '1'
    }
  },
  created () {
    this.getInfo()
  },
  methods: {
    // 每页显示的条数改变
    handleSizeChange (val) {
      this.size = val // 改变每页显示的条数
      this.page = 1 // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.getInfo() // 点击每页显示的条数时，显示第一页
      console.log(`每页 ${val} 条`)
    },

    // current-change用于监听页数改变，而内容也发生改变
    handleCurrentChange (val) {
      this.page = val // 改变默认的页数
      this.getInfo() // 切换页码时，要获取每页显示的条数
      console.log(`当前页: ${val}`)
    },

    // 查询信息
    async getInfo () {
      if (this.starttime != null || this.endtime != null) {
        this.$axios.get(this.url + this.log_type + '&size=' + this.count + '&page=' + this.page + '&start_time=' + this.starttime + '&end_time=' + this.endtime)
          .then(response => {
            this.tableData = response.data.results
            this.count = response.data.count
          })
          .catch(error => {
            console.log(error)
          })
      } else {
        this.$axios.get(this.url + this.log_type + '&size=' + this.size + '&page=' + this.page)
          .then(response => {
            this.tableData = response.data.results
            this.count = response.data.count
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    select () {
      if (this.timeForm.queryTime != null) {
        this.starttime = this.timeForm.queryTime[0]
        this.endtime = this.timeForm.queryTime[1]
      } else {
        this.starttime = null
        this.endtime = null
      }
      this.getInfo()
    }
  }
}
</script>

<style scoped>
</style>
