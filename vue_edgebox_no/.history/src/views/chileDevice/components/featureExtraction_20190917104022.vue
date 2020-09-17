<template>
  <el-main class="no-padding">
    <el-row>
      <!-- 基本信息 -->
      <el-col :span="{xs: 12, sm: 12,  md: 12, lg: 12, xl: 12}">
        <el-card>
          <el-form :model="baseForm" label-width="80px" label-position="left">
            <el-form-item label="名称:">
              <span>{{baseForm.name}}</span>
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
        templateName: '',
        serial: 'com3',
        dataBit: '',
        baudRate: '',
        parity: '',
        stopBit: '',
        timeout: '',
        cycle: '',
        address: '',
        drive: ''
      }
    }
  },
}
</script>

<style scoped>

</style>
