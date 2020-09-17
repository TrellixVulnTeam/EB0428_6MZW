<template>
  <el-main>
      <el-row class="row-padding">
          <el-select v-model="interfaceType">
              <el-option v-for="item in typeList" :key="item.index" :value="item.index" :label="item.value"></el-option>
          </el-select>
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
                index: 1,
                value: '以太网类型'   
            },
            {
                index: 2,
                value: '专有类型'   
            }
        ]
    }
  },
}
</script>

<style scoped>

</style>
