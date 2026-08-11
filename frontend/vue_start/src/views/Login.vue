<template>
  <div class="login-page">
    <div class="login-box">
      <h2>用户登录</h2>

      <input
        v-model="username"
        placeholder="请输入用户名"
      />
      <br><br>

      <input
        v-model="password"
        type="password"
        placeholder="请输入密码"
      />
      <div class="tip-text">
        没有账号？<span class="register-link" @click="goRegister">请先注册</span>
      </div>
      <br>

      <button @click="loginUser">
        登录
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/user'
import { useUserStore } from '../stores/user'

const username = ref('')
const password = ref('')
const userStore = useUserStore()
const router = useRouter()


const goRegister = () => {
  router.push('/register')
}

const loginUser = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    alert('用户名和密码不能为空！')
    return
  }

  try {
    const res = await login({
      username: username.value,
      password: password.value
    })

    if (!res.data.token) {
      alert(res.data.message || '登录失败')
      return
    }

    userStore.setUser({
      token: res.data.token,
      username: res.data.username
    })
    alert('登录成功！')
    router.push('/home')

  } catch (error) {
    console.error(error)
    alert(error.response?.data?.detail || '账号或密码错误')
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: 0;
}
.login-box {
  text-align: center;
  width: 350px;
  padding: 40px;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
input {
  width: 100%;
  padding: 8px 12px;
  box-sizing: border-box;
}
button {
  padding: 10px 20px;
  width: 100%;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
/* 新增样式 */
.tip-text {
  font-size: 13px;
  color: #666;
  margin-top: 6px;
}
.register-link {
  color: #42b983;
  cursor: pointer;
}
.register-link:hover {
  text-decoration: underline;
}
</style>