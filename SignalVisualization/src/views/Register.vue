<template>
  <div class="auth-page">
    <section class="auth-summary">
      <span class="system-label">Account Provisioning</span>
      <h1>创建操作员账号</h1>
      <p>注册后默认获得操作员权限，可访问监控大屏和仿真优化模块。</p>
    </section>

    <section class="auth-card">
      <h2>账号注册</h2>
      <p class="subtitle">请填写登录信息</p>

      <form @submit.prevent="handleRegister">
        <label>
          用户名
          <input v-model="username" type="text" autocomplete="username" placeholder="设置用户名" required />
        </label>

        <label>
          密码
          <input v-model="password" type="password" autocomplete="new-password" placeholder="设置密码" required />
        </label>

        <label>
          确认密码
          <input v-model="confirmPassword" type="password" autocomplete="new-password" placeholder="再次输入密码" required />
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册账号' }}
        </button>

        <p v-if="error" class="message error">{{ error }}</p>
        <p v-if="success" class="message success">{{ success }}</p>

        <p class="auth-link">
          已有账号？<router-link to="/login">返回登录</router-link>
        </p>
      </form>
    </section>
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
    await axios.post('./api/auth/register', {
      username: username.value,
      password: password.value,
      role: 'operator'
    })
    success.value = '注册成功，正在跳转到登录页...'
    setTimeout(() => router.push('/login'), 1600)
  } catch (err: any) {
    error.value = err.response?.data?.msg || '注册失败，用户名可能已存在'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  background: #f4f6f8;
  color: #1f2933;
}

.auth-summary {
  padding: 72px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-right: 1px solid #d8dee6;
}

.system-label {
  color: #52606d;
  font-size: 13px;
}

h1 {
  max-width: 560px;
  margin: 12px 0 16px;
  font-size: 36px;
  line-height: 1.25;
}

.auth-summary p {
  margin: 0;
  color: #52606d;
  font-size: 16px;
}

.auth-card {
  align-self: center;
  margin: 32px;
  padding: 32px;
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 6px;
}

h2 {
  margin: 0;
  font-size: 22px;
}

.subtitle {
  margin: 8px 0 24px;
  color: #697586;
}

label {
  display: block;
  margin-bottom: 16px;
  color: #344054;
  font-size: 14px;
  font-weight: 600;
}

input {
  width: 100%;
  box-sizing: border-box;
  margin-top: 8px;
  padding: 11px 12px;
  border: 1px solid #cbd2d9;
  border-radius: 4px;
  background: #fff;
  color: #1f2933;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #2457a6;
  box-shadow: 0 0 0 3px rgba(36, 87, 166, 0.12);
}

button {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #2457a6;
  border-radius: 4px;
  background: #2457a6;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  border-color: #cbd2d9;
  background: #cbd2d9;
  cursor: not-allowed;
}

.message {
  margin: 14px 0 0;
  font-size: 14px;
}

.error { color: #a61b1b; }
.success { color: #217a3d; }

.auth-link {
  margin: 20px 0 0;
  color: #697586;
  text-align: center;
  font-size: 14px;
}

.auth-link a {
  color: #2457a6;
  text-decoration: none;
  font-weight: 700;
}

@media (max-width: 820px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-summary {
    padding: 36px 28px 0;
    border-right: 0;
  }

  .auth-card {
    margin: 28px;
  }
}
</style>
