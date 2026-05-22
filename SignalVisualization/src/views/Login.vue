<template>
  <div class="auth-page">
    <section class="auth-summary">
      <div class="brand-block">
        <span class="brand-mark"></span>
        <div>
          <span class="system-label">Signal Monitoring Console</span>
          <h1>西藏高原移动信号分析平台</h1>
        </div>
      </div>
      <p>面向采样、监控、仿真和优化报告的内部业务系统。</p>

      <div class="status-panel">
        <div class="status-head">
          <span>平台状态</span>
          <strong>运行中</strong>
        </div>
        <dl>
          <div>
            <dt>采样任务</dt>
            <dd>拉萨城区</dd>
          </div>
          <div>
            <dt>监测设备</dt>
            <dd>24 / 30 在线</dd>
          </div>
          <div>
            <dt>数据范围</dt>
            <dd>RSRP / SINR / 海拔</dd>
          </div>
        </dl>
      </div>
    </section>

    <section class="auth-card">
      <div class="card-head">
        <div>
          <h2>账号登录</h2>
          <p class="subtitle">请输入平台账号和密码</p>
        </div>
        <span class="security-tag">内部访问</span>
      </div>

      <form @submit.prevent="handleLogin">
        <label>
          用户名
          <input v-model="username" type="text" autocomplete="username" placeholder="请输入用户名" required />
        </label>

        <label>
          密码
          <input v-model="password" type="password" autocomplete="current-password" placeholder="请输入密码" required />
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录系统' }}
        </button>

        <p v-if="error" class="message error">{{ error }}</p>

        <p class="auth-link">
          没有账号？<router-link to="/register">注册操作员账号</router-link>
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
const loading = ref(false)
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const res = await axios.post('/api/auth/login', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.msg || '登录失败，请检查账号、密码或后端服务状态'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 440px;
  background:
    linear-gradient(90deg, rgba(248, 250, 252, 0.96), rgba(248, 250, 252, 0.86)),
    repeating-linear-gradient(0deg, transparent 0, transparent 31px, rgba(203, 210, 217, 0.34) 32px),
    repeating-linear-gradient(90deg, transparent 0, transparent 31px, rgba(203, 210, 217, 0.28) 32px);
  color: #1f2933;
}

.auth-summary {
  padding: 72px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-right: 1px solid #d8dee6;
}

.brand-block {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.brand-mark {
  width: 14px;
  height: 54px;
  margin-top: 5px;
  display: inline-block;
  border-radius: 2px;
  background: #2457a6;
  box-shadow: inset 0 -18px 0 #183b70;
}

.system-label {
  color: #52606d;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

h1 {
  max-width: 560px;
  margin: 10px 0 16px;
  font-size: 40px;
  line-height: 1.25;
}

.auth-summary p {
  margin: 0;
  color: #52606d;
  font-size: 16px;
  line-height: 1.8;
}

.status-panel {
  width: min(560px, 100%);
  margin-top: 42px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid #d8dee6;
  border-radius: 8px;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
}

.status-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid #e4e7eb;
}

.status-head span {
  font-size: 15px;
  font-weight: 700;
}

.status-head strong {
  padding: 4px 8px;
  border-radius: 4px;
  background: #e3f8eb;
  color: #217a3d;
  font-size: 12px;
}

dl {
  margin: 16px 0 0;
  display: grid;
  gap: 14px;
}

dt {
  color: #697586;
  font-size: 13px;
}

dd {
  margin: 5px 0 0;
  color: #1f2933;
  font-size: 15px;
  font-weight: 700;
}

.auth-card {
  align-self: center;
  margin: 32px;
  padding: 34px;
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 8px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.12);
}

.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 26px;
}

h2 {
  margin: 0;
  font-size: 22px;
}

.subtitle {
  margin: 8px 0 0;
  color: #697586;
}

.security-tag {
  flex-shrink: 0;
  padding: 4px 8px;
  border-radius: 4px;
  background: #edf2f7;
  color: #52606d;
  font-size: 12px;
  font-weight: 700;
}

label {
  display: block;
  margin-bottom: 18px;
  color: #344054;
  font-size: 14px;
  font-weight: 600;
}

input {
  width: 100%;
  box-sizing: border-box;
  margin-top: 8px;
  padding: 12px 13px;
  border: 1px solid #cbd2d9;
  border-radius: 4px;
  background: #fbfdff;
  color: #1f2933;
  font-size: 14px;
  transition: border-color 0.16s ease, box-shadow 0.16s ease, background-color 0.16s ease;
}

input:focus {
  outline: none;
  border-color: #2457a6;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(36, 87, 166, 0.12);
}

button {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #2457a6;
  border-radius: 4px;
  background: #2457a6;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.16s ease, border-color 0.16s ease;
}

button:hover:not(:disabled) {
  border-color: #183b70;
  background: #183b70;
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

.error {
  color: #a61b1b;
}

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

  h1 {
    font-size: 30px;
  }

  .auth-card {
    margin: 28px;
  }
}
</style>
