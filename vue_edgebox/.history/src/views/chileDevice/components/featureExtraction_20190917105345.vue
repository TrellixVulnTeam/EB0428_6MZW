<template>
  <el-main class="no-padding">
    <el-row>
      <!-- 基本信息 -->
      <el-col :span="{xs: 12, sm: 12,  md: 12, lg: 12, xl: 12}">
        <el-card class="card-style">
          <el-form :model="baseForm" label-width="80px" label-position="left">
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="类型:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="位置:">
              <span>{{baseForm.name}}</span>
            </el-form-item>
            <el-form-item label="模板名称:">
              <el-button type="text" size="small">去配置协议</el-button>
            </el-form-item>
            <el-form-item label="串口号:">
              <span>{{baseForm.serial}}</span>
            </el-form-item>
            <el-form-item label="数据位:">
              <span>{{baseForm.dataBit}}</span>
            </el-form-item>
            <el-form-item label="波特率:">
              <span>{{baseForm.baudRate}}</span>
            </el-form-item>
            <el-form-item label="奇偶校验:">
              <span>{{baseForm.parity}}</span>
            </el-form-item>
            <el-form-item label="停止位:">
              <span>{{baseForm.stopBit}}</span>
            </el-form-item>
            <el-form-item label="回复超时:">
              <span>{{baseForm.timeout}}</span>
            </el-form-item>
            <el-form-item label="读写周期:">
              <span>{{baseForm.cycle}}</span>
            </el-form-item>
            <el-form-item label="地址码:">
              <span>{{baseForm.address}}</span>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <!-- 特征数据 -->
      <el-col :span="{xs: 12, sm: 12,  md: 12, lg: 12, xl: 12}">

      </el-col>
    </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      baseForm: {
        name: 'Lichang90011',
        type: '力创电表',
        position: 'E5-4F',
        // templateName: '',
        serial: 'com3',
        dataBit: 8,
        baudRate: '9600',
        parity: 'o（奇校验）',
        stopBit: 2,
        timeout: '5s',
        cycle: '10s',
        address: '02'
      }
    }
  },
}
</script>

<style scoped>
.card-style {
  min-width: 400px;
  width: 100%;
}
</style>
