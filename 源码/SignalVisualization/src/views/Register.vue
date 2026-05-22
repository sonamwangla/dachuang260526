<template>
  <div class="login-container">
    <div class="login-box">
      <h2>加入信号分析系统</h2>
      <p class="subtitle">创建您的操作员账户</p>
      
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label>用户名</label>
          <input type="text" v-model="username" placeholder="请设置用户名" required />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请设置密码" required />
        </div>
        <div class="input-group">
          <label>确认密码</label>
          <input type="password" v-model="confirmPassword" placeholder="请再次输入密码" required />
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? '正在注册...' : '立即注册' }}
        </button>
        
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>

        <div class="footer-links">
          已有账号？ <router-link to="/login">返回登录</router-link>
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
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const router = useRouter()

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/auth/register', {
      username: username.value,
      password: password.value,
      role: 'operator' // 默认注册为操作员
    })
    success.value = '注册成功！正在跳转登录...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    error.value = err.response?.data?.msg || '注册失败，用户名可能已存在'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle at center, #001a35 0%, #000c17 100%);
  color: #fff; font-family: 'Inter', sans-serif;
}
.login-box {
  width: 400px; padding: 40px; background: rgba(0, 21, 41, 0.8);
  border: 1px solid rgba(24, 144, 255, 0.3); border-radius: 8px;
  backdrop-filter: blur(10px); box-shadow: 0 0 40px rgba(0,0,0,0.5);
}
h2 { margin: 0; color: #1890ff; text-align: center; }
.subtitle { text-align: center; color: #a6adb4; font-size: 14px; margin-bottom: 30px; }
.input-group { margin-bottom: 20px; }
label { display: block; margin-bottom: 8px; font-size: 14px; color: #e6f7ff; }
input {
  width: 100%; padding: 12px; background: rgba(0,0,0,0.3); border: 1px solid #333;
  border-radius: 4px; color: #fff; box-sizing: border-box;
}
input:focus { outline: none; border-color: #1890ff; }
button {
  width: 100%; padding: 12px; background: #52c41a; color: #fff; border: none;
  border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px; transition: 0.3s;
}
button:hover { background: #73d13d; }
button:disabled { background: #555; cursor: not-allowed; }
.error-msg { color: #ff4d4f; font-size: 14px; text-align: center; margin-top: 15px; }
.success-msg { color: #52c41a; font-size: 14px; text-align: center; margin-top: 15px; }
.footer-links { margin-top: 20px; text-align: center; font-size: 14px; color: #8c8c8c; }
.footer-links a { color: #1890ff; text-decoration: none; }
</style>
