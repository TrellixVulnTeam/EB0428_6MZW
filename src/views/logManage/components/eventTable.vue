<template>
  <el-main class="no-padding">

      <el-row class="row-padding">
          <el-input size="small" placeholder="请输入内容" v-model="searchEvent" class="search-input pull-right">
           <el-button slot="append" icon="el-icon-search" @click="select()"></el-button>
         </el-input>
      </el-row>
      <el-table :data="tableData">
          <el-table-column label="事件类型" prop="event_type" sortable>
            <template slot-scope="scope">
              <el-tag
                :type="scope.row.event_type === '報警' ? 'danger' : 'success'"
                disable-transitions>{{scope.row.event_type}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="记录时间" prop="event_create_time" sortable></el-table-column>
          <el-table-column label="事件详情" prop="event_info" sortable></el-table-column>
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
export default {
  data () {
    return {
      page: 1, // 当前页
      count: 1, // 记录
      size: 10, // 每页条数
      url: '/apis/loginfo/Event_list/?size=',
      searchEvent: null,
      tableData: []
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
    this.$axios.get(this.url + this.size)
      .then(response => {
        this.tableData = response.data.results
        this.count = response.data.count
      })
      .catch(error => {
        console.log(error)
      })
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
      if (this.searchEvent != null) {
        this.$axios.get(this.url + this.count + '&search=' + this.searchEvent)
          .then(response => {
            this.tableData = response.data.results
            this.count = response.data.count
          })
          .catch(error => {
            console.log(error)
          })
      } else {
        this.$axios.get(this.url + this.size + '&page=' + this.page)
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
      this.getInfo()
    }
  }
}
</script>

<style scoped>
</style>
