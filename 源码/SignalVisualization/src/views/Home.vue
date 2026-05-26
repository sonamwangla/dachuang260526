<template>
  <div class="home-container">
    <!-- 1. 顶部导航栏 -->
    <nav class="top-nav">
      <div class="logo">
        <span class="logo-icon">📡</span>
        <span class="logo-text">西藏信号分析 V2.0</span>
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/visualization">监控大屏</router-link>
        <router-link v-if="['admin', 'operator'].includes(user.role)" to="/optimization">仿真中心</router-link>
        <span class="user-info">
          <span class="role-badge" :class="user.role">{{ roleName }}</span>
          <span class="uname">{{ user.username }}</span>
          <button @click="handleLogout" class="logout-btn">退出</button>
        </span>
      </div>
    </nav>

    <!-- 2. Hero 展示区 -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="badge fade-in">Tibet Signal Intelligence</div>
        <h1 class="main-title">西藏高原移动信号<br/><span class="highlight">智能分析与可视化平台</span></h1>
        <p class="description">
          集成 AI 随机森林模型与高原物理衰减算法，提供 3D 数字孪生仿真、实时信号监测及闭环优化建议。
        </p>
        <div class="cta-actions">
          <router-link to="/visualization" class="btn primary-btn">进入监控大屏</router-link>
          <router-link v-if="['admin', 'operator'].includes(user.role)" to="/optimization" class="btn secondary-btn">进入 3D 仿真中心</router-link>
          <div v-else class="locked-feature">🔒 仿真中心仅限技术人员访问</div>
        </div>
      </div>
    </section>

    <!-- 3. 找回丢失的统计条 -->
    <section class="stats-bar shadow-sm">
      <div class="stat-item">
        <span class="stat-num">5,000+</span>
        <span class="stat-label">监测采集点位</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">3,650m</span>
        <span class="stat-label">平均监测海拔</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">94.2%</span>
        <span class="stat-label">AI 预测准确率</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">24/7</span>
        <span class="stat-label">全天候监测</span>
      </div>
    </section>

    <!-- 4. 找回丢失的核心功能卡片 -->
    <section class="features-section">
      <h2 class="section-title">核心业务模块</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="f-icon">📊</div>
          <h3>实时三维监控</h3>
          <p>基于 GIS 引擎，实时呈现高原复杂地形下的信号热力分布图与设备采集轨迹。</p>
        </div>
        <div class="feature-card">
          <div class="f-icon">🤖</div>
          <h3>AI 仿真分析</h3>
          <p>利用 RandomForest 模型预判极弱信号覆盖风险，支持海拔与天气因素的复合评估。</p>
        </div>
        <div class="feature-card">
          <div class="f-icon">✅</div>
          <h3>PDF 决策报告</h3>
          <p>一键生成专业级诊断报告，包含 3D 分布图、信号指标分析及专家级优化建议。</p>
        </div>
      </div>
    </section>

    <footer class="main-footer">
      <p>© 2026 西藏高原地区移动信号智能优化与可视化平台 | 当前角色: {{ roleName }}</p>
    </footer>

    <!-- 访客友好提示 -->
    <div v-if="showLockTip" class="access-tip shadow fade-in">
      ⚠️ 访客权限仅支持数据查阅。若需仿真优化功能，请联系管理员。
      <button @click="showLockTip = false" class="close-btn">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(JSON.parse(localStorage.getItem('user') || '{"username": "Guest", "role": "viewer"}'))
const showLockTip = ref(false)

const roleName = computed(() => {
  const map: any = { 'admin': '超级管理员', 'operator': '技术操作员', 'viewer': '访客观察员' }
  return map[user.role] || '未知角色'
})

const handleLogout = () => {
  localStorage.removeItem('token'); localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  if (user.role === 'viewer') setTimeout(() => { showLockTip.value = true }, 1500)
})
</script>

<style scoped>
.home-container { min-height: 100vh; background: #ffffff; color: #333; font-family: 'Inter', sans-serif; overflow-x: hidden; }
.top-nav { height: 75px; padding: 0 10%; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e8e8e8; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); position: sticky; top: 0; z-index: 100; }
.logo-text { font-weight: bold; font-size: 1.3rem; color: #1890ff; }
.nav-links { display: flex; gap: 35px; align-items: center; }
.nav-links a { text-decoration: none; color: #666; font-weight: 500; font-size: 0.95rem; transition: 0.3s; }
.nav-links a:hover { color: #1890ff; }
.user-info { display: flex; align-items: center; gap: 12px; font-size: 0.9rem; padding-left: 20px; border-left: 1px solid #e8e8e8; }
.role-badge { padding: 2px 10px; border-radius: 4px; color: #fff; font-size: 0.75rem; font-weight: bold; }
.role-badge.admin { background: #ff4d4f; }
.role-badge.operator { background: #1890ff; }
.role-badge.viewer { background: #595959; }
.uname { color: #333; font-weight: 600; }
.logout-btn { cursor: pointer; border: 1px solid #d9d9d9; background: transparent; color: #666; border-radius: 4px; padding: 2px 10px; font-size: 0.8rem; transition: 0.3s; }
.logout-btn:hover { border-color: #ff4d4f; color: #ff4d4f; }

.hero-section { padding: 120px 10% 100px; text-align: center; background: #f5f7fa; position: relative; }
.hero-section::after { content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 100px; background: linear-gradient(to bottom, transparent, #ffffff); }
.badge { display: inline-block; padding: 5px 15px; background: rgba(24,144,255,0.1); border: 1px solid #1890ff; color: #1890ff; border-radius: 20px; font-size: 0.8rem; margin-bottom: 25px; letter-spacing: 1px; }
.main-title { font-size: 3.8rem; font-weight: 800; color: #333; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1px; }
.highlight { color: #1890ff; }
.description { max-width: 800px; margin: 0 auto 60px; color: #666; font-size: 1.25rem; line-height: 1.8; }
.cta-actions { display: flex; gap: 20px; justify-content: center; position: relative; z-index: 10; }
.btn { padding: 16px 45px; border-radius: 8px; text-decoration: none; font-weight: bold; transition: 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); cursor: pointer; }
.primary-btn { background: #1890ff; color: #fff; box-shadow: 0 8px 25px rgba(24,144,255,0.3); }
.primary-btn:hover { transform: translateY(-5px); box-shadow: 0 12px 35px rgba(24,144,255,0.4); background: #40a9ff; }
.secondary-btn { border: 2px solid #1890ff; color: #1890ff; background: rgba(24,144,255,0.05); }
.secondary-btn:hover { background: rgba(24,144,255,0.1); transform: translateY(-5px); }

.stats-bar { display: grid; grid-template-columns: repeat(4, 1fr); padding: 80px 10%; background: #ffffff; border-top: 1px solid #e8e8e8; }
.stat-num { display: block; font-size: 3.2rem; font-weight: 800; color: #1890ff; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace; }
.stat-label { font-size: 0.95rem; color: #666; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }

.features-section { padding: 100px 10%; background: #ffffff; }
.section-title { text-align: center; margin-bottom: 80px; font-size: 2.4rem; font-weight: 800; color: #333; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.feature-card { padding: 60px 40px; background: #fafafa; border: 1px solid #e8e8e8; border-radius: 20px; transition: 0.4s; text-align: center; position: relative; overflow: hidden; }
.feature-card:hover { transform: translateY(-15px); background: rgba(24,144,255,0.05); border-color: #1890ff; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.feature-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #1890ff, transparent); opacity: 0; transition: 0.4s; }
.feature-card:hover::before { opacity: 1; }
.f-icon { font-size: 4rem; margin-bottom: 35px; }
.feature-card h3 { font-size: 1.5rem; color: #333; margin-bottom: 20px; }
.feature-card p { font-size: 1rem; color: #666; line-height: 1.8; }

.main-footer { padding: 60px; text-align: center; border-top: 1px solid #e8e8e8; color: #666; font-size: 0.9rem; }
.fade-in { animation: fadeIn 1s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
</style>
