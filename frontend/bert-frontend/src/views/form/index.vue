<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="写下你的意见">
        <el-input v-model="form.feedback" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="onCancel">清空</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      List: [],
      form: {
        feedback: ''
      }
    }
  },
  methods: {
    onSubmit() {
      if (this.form.feedback === '') {
        this.$message({
          message: '内容不能为空',
          type: 'error'
        })
      } else {
        this.axios.post('/api/submit_feedback', {
          feedback: this.form.feedback
        })
          .then((response) => {
            this.$message({
              message: '提交成功',
              type: 'success'
            })
            this.form.feedback = ''
          })
      }
    },
    onCancel() {
      this.form.feedback = ''
      this.$message({
        message: '清空成功',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

