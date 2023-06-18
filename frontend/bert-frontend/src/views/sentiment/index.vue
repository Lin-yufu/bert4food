<template>
  <div class="dashboard-container">
    <div id="dashboard-content">
      <el-row>
        <el-col :span="6" style="padding: 10px;">
      <el-card>
        <div>总评论数：</div>
        <div style="padding: 10px; font-weight: bold">{{ positiveNum+negativeNum }}</div>
      </el-card>
      </el-col>
      <el-col :span="6" style="padding: 10px;">
      <el-card>
        <div>积极评价数：</div>
        <div style="padding: 10px; font-weight: bold">{{ positiveNum }}</div>
      </el-card>
      </el-col>
      <el-col :span="6" style="padding: 10px;">
      <el-card>
        <div>消极评价数：</div>
        <div style="padding: 10px; font-weight: bold">{{ negativeNum }}</div>
      </el-card>
      </el-col>
      </el-row>
      <el-row>
        <div id="pie" style="padding: 30px; width: 600px;height:400px;" />
      </el-row>
      </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'Dashboard',
  data() {
    return {
      positiveNum: 0,
      negativeNum: 0

    }
  },
  mounted() {
    this.drawPie()
    this.getData()
  },
  methods: {
    drawPie() {
      var chartDom = document.getElementById('pie')
      var myChart = echarts.init(chartDom)
      var option
      option = {
        series: [
          {
            type: 'pie',
            data: [
              {
                value: this.positiveNum,
                name: '积极评价'
              },
              {
                value: this.negativeNum,
                name: '消极评价'
              }
            ]
          }
        ]
      }
      myChart.setOption(option)
    },
    getData() {
      this.axios.get('/api/get_feedback_num').then((response) => {
        this.positiveNum = response.data.positive
        this.negativeNum = response.data.negative
      })
    }
  }}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
