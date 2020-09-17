<template>
  <el-main>
      <el-row class="row-padding">
          <el-select v-model="interfaceType">
      </el-row>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
        interfaceType: '',
        typeList: [
            {
                index: 0,
                value: 'RS232接口类'   
            },
            {
                index: 0,
                value: 'RS232接口类'   
            },
            {
                index: 0,
                value: 'RS232接口类'   
            }
        ]
    }
  },
}
</script>

<style scoped>

</style>
