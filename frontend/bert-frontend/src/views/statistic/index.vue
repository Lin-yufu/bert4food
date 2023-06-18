<template>
  <div class="dashboard-container">
    <div id="dashboard-content">
      <el-row>
        <el-col :span="8" style="margin-right: 10px">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>消极评论关键词</span>
            </div>
            <div>
              <img class="wordcloud" :src="negativeWordCloud" />
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>积极评论关键词</span>
            </div>
            <div>
              <img class="wordcloud" :src="positiveWordCloud" />
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-row id="button">
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">刷新关键词</el-button>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      negativeWordCloud: 'http://127.0.0.1:5000/static/negative.jpg',
      positiveWordCloud: 'http://127.0.0.1:5000/static/positive.jpg'
    }
  },
  methods: {
    refresh() {
      this.getWordCloud()
    },
    getWordCloud() {
      this.axios.get('/api/get_wordcloud').then((response) => {
        this.positiveWordCloud = response.data.positive
        this.negativeWordCloud = response.data.negative
      })
    }
  }
}
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
.wordcloud {
  height: 400px;
  width: 400px;
}
.title {
  margin: 0 auto;
  text-align: center;
}
#button{
  padding-top: 20px;
}
</style>
