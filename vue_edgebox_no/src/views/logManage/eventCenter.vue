<template>
  <el-main class="no-padding">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>事件中心</el-breadcrumb-item>
        <el-breadcrumb-item>消息</el-breadcrumb-item>
      </el-breadcrumb>
      <el-row class="row-padding">
          <el-button type="primary" size="small" >查看最近一周</el-button>
          <el-input size="small" placeholder="请输入内容" v-model="searchEvent" class="search-input pull-right">
           <el-button slot="append" icon="el-icon-search"></el-button>
         </el-input>
      </el-row>
      <el-table
      :data="tableData"
      style="width: 100%"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="id"
        label="序号"
        min-width="10%">
      </el-table-column>
      <el-table-column
        :filters="[{ text: 'info', value: 'info' }, { text: 'warning', value: 'warning' }, { text: 'success', value: 'success' }, { text: 'error', value: 'error' }]"
        :filter-method="filterTag"
        prop="event_level"
        label="事件等级"
        min-width="15%">
      </el-table-column>
      <el-table-column
        sortable
        prop="create_time"
        label="触发时间"
        min-width="25%">
      </el-table-column>
      <el-table-column
        prop="event_username"
        label="用户操作"
        min-width="10%">
      </el-table-column>
      <el-table-column
        prop="event_remark"
        label="事件详情"
        min-width="30%">
      </el-table-column>
       <el-table-column
        fixed="right"
        label="操作"
         min-width="10%">
        <template slot-scope="scope">
          <el-button
            @click.native.prevent="deleteRow(scope.$index, tableData)"
            type="text"
            size="small">
            移除
          </el-button>
        </template>
    </el-table-column>
  </el-table>
  </el-main>
</template>

<script>
export default {
  methods: {
      tableRowClassName({row, rowIndex}) {
        if (row.event_level === "warning") {
          return 'warning-row';
        } else if (row.event_level === "success") {
          return 'success-row';
        }
        else if (row.event_level === "error") {
          return 'error-row';
        }
        return '';
      },
      filterTag(value, row) {
        return row.event_level === value;
      },
      getevent(){
         this.$axios.get("apis/log/event/")
          .then(response => {
            this.tableData = response.data.event
          })
          this.loading = false;
      },
       deleteRow(index, rows) {
        var _this = this;
        this.$axios.post('apis/log/delete/', {
          event_no: rows[index]["id"],
        })
        .then(function (response) {
          console.log(response.data.message);
          rows.splice(index, 1);
          _this.$Message.SuccessMessage(_this, response.data.message);
          // _this.flush_status()
        })
        .catch(function (error) {
          console.log(error);
        });
      }

    },
  created() {
    this.getevent()
  },
  data() {
    return {
        searchEvent: '',
        tableData: [
            {
                id: 1,
                event_level: 'info',
                event_username: 'admin',
                create_time: '2019/05/02 02:22',
                event_remark: 'dirtimealsdidfdfcdtime'
            }
        ]
    }
  },
}
</script>

<style >
.el-table .warning-row {
    background: oldlace;
  }

.el-table .success-row {
  background: #f0f9eb;
}

.el-table .error-row {
  background: #e23f38;
}
</style>
