<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <div class="form-item">
      <label>用户名：</label>
      <input v-model="form.username" type="text" placeholder="请输入用户名" />
    </div>
    <div class="form-item">
      <label>密码：</label>
      <input v-model="form.password" type="password" placeholder="请输入密码" />
    </div>
    <div class="form-item">
      <label>邮箱：</label>
      <input v-model="form.email" type="email" placeholder="请输入邮箱" />
    </div>
    <button @click="submitRegister">立即注册</button>
    <div class="tip-text">
      已有账号？<span class="login-link" @click="goLogin">去登录</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/user'

// 注册表单数据
const form = ref({
  username: '',
  password: '',
  email: ''
})
const router = useRouter()

// 跳转到登录页
const goLogin = () => {
  router.push('/login')
}

// 提交注册
const submitRegister = async () => {
  if (!form.value.username.trim() || !form.value.password.trim() || !form.value.email.trim()) {
    alert('用户名、密码和邮箱不能为空！')
    return
  }

  try {
    const res = await register(form.value)
    alert('注册成功！')
    console.log(res.data)
    router.push('/login')
  } catch (err) {
    alert('注册失败：' + (err.response?.data?.detail || '服务器错误'))
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
}
.form-item {
  margin: 15px 0;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px 20px;
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}
/* 跳转文字样式 */
.tip-text {
  text-align: center;
  margin-top: 15px;
  font-size: 13px;
  color: #666;
}
.login-link {
  color: #42b983;
  cursor: pointer;
}
.login-link:hover {
  text-decoration: underline;
}
</style>