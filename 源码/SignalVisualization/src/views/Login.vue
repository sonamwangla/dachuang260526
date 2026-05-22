<template>
  <div class="login-container">
    <div class="login-box">
      <h2>西藏高原信号分析系统</h2>
      <p class="subtitle">智能监测与优化平台</p>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>用户名</label>
          <input type="text" v-model="username" placeholder="请输入用户名" required />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请输入密码" required />
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? '正在登录...' : '登录系统' }}
        </button>
        
        <p v-if="error" class="error-msg">{{ error }}</p>
        
        <div class="footer-links">
          没有账号？ <router-link to="/register">立即注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/auth/login', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.msg || '登录失败，请检查网络或凭据'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: #f5f7fa;
  color: #333; font-family: 'Inter', sans-serif;
}
.login-box {
  width: 400px; padding: 40px; background: #ffffff;
  border: 1px solid #e8e8e8; border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
h2 { margin: 0; color: #1890ff; text-align: center; }
.subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 30px; }
.input-group { margin-bottom: 20px; }
label { display: block; margin-bottom: 8px; font-size: 14px; color: #666; }
input {
  width: 100%; padding: 12px; background: #fafafa; border: 1px solid #d9d9d9;
  border-radius: 4px; color: #333; box-sizing: border-box;
}
input:focus { outline: none; border-color: #1890ff; }
button {
  width: 100%; padding: 12px; background: #1890ff; color: #fff; border: none;
  border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; transition: 0.3s;
}
button:hover { background: #40a9ff; }
button:disabled { background: #d9d9d9; cursor: not-allowed; }
.error-msg { color: #ff4d4f; font-size: 14px; text-align: center; margin-top: 15px; }
.footer-links { margin-top: 20px; text-align: center; font-size: 14px; color: #666; }
.footer-links a { color: #1890ff; text-decoration: none; }
</style>
