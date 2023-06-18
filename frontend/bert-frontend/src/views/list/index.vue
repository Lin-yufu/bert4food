<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="发表时间" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column label="评价内容">
        <template slot-scope="scope">
          <span>{{ scope.row.comment }}</span>
        </template>
      </el-table-column>
      <el-table-column label="情感倾向" width="150" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.sentiment | statusFilter">{{ showSentiment(scope.row.sentiment) }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        1: 'success',
        0: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      this.axios.get('/api/get_feedback_list').then((response) => {
        this.list = response.data
        this.listLoading = false
      })
    },
    showSentiment(status) {
      console.log(status)
      if (status === 0) {
        return '消极评价'
      } else return '积极评价'
    }
  }
}
</script>
