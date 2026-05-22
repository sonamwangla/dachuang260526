<template>
  <div class="home-page">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div>
          <strong>西藏高原移动信号分析平台</strong>
          <span>Signal Monitoring Console</span>
        </div>
      </div>

      <nav class="nav">
        <router-link to="/">概览</router-link>
        <router-link to="/visualization">监控大屏</router-link>
        <router-link v-if="canOperate" to="/optimization">仿真优化</router-link>
      </nav>

      <div class="account">
        <span class="role" :class="user.role">{{ roleName }}</span>
        <span class="username">{{ user.username }}</span>
        <button type="button" @click="handleLogout">退出</button>
      </div>
    </header>

    <main class="content">
      <section class="overview">
        <div class="overview-copy">
          <span class="eyebrow">拉萨城区及周边采样任务</span>
          <h1>移动信号覆盖监测与优化分析</h1>
          <p>
            汇总采样点、基站、RSRP 和海拔环境数据，支持弱覆盖定位、历史回放和仿真参数评估。
          </p>
          <div class="actions">
            <router-link class="primary" to="/visualization">进入监控大屏</router-link>
            <router-link v-if="canOperate" class="secondary" to="/optimization">打开仿真优化</router-link>
          </div>
        </div>

        <div class="task-panel">
          <div class="panel-head">
            <span>今日任务</span>
            <strong>运行中</strong>
          </div>
          <dl>
            <div>
              <dt>采样点位</dt>
              <dd>5,000+</dd>
            </div>
            <div>
              <dt>平均海拔</dt>
              <dd>3,650 m</dd>
            </div>
            <div>
              <dt>预测准确率</dt>
              <dd>94.2%</dd>
            </div>
            <div>
              <dt>监测时段</dt>
              <dd>24 h</dd>
            </div>
          </dl>
        </div>
      </section>

      <section class="modules">
        <article>
          <span class="module-index">01</span>
          <h2>实时覆盖监控</h2>
          <p>地图侧重呈现弱覆盖、运营商差异和采样轨迹，便于快速定位异常区域。</p>
        </article>
        <article>
          <span class="module-index">02</span>
          <h2>高原环境建模</h2>
          <p>将海拔、地形遮挡、气象损耗等因素纳入预测，辅助判断信号衰减原因。</p>
        </article>
        <article>
          <span class="module-index">03</span>
          <h2>优化处置闭环</h2>
          <p>面向管理员和操作员输出仿真结果、报告和参数调整建议，减少人工整理成本。</p>
        </article>
      </section>

      <section v-if="showPermissionNotice" class="notice">
        当前账号没有仿真优化权限。请使用管理员或操作员账号登录。
      </section>
    </main>

    <footer class="footer">
      <span>当前角色：{{ roleName }}</span>
      <span>西藏高原移动信号模拟优化与可视化平台</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const user = ref(JSON.parse(localStorage.getItem('user') || '{"username":"Guest","role":"viewer"}'))

const roleName = computed(() => {
  const map: Record<string, string> = {
    admin: '管理员',
    operator: '操作员',
    viewer: '观察员'
  }
  return map[user.value.role] || '未知角色'
})

const canOperate = computed(() => ['admin', 'operator'].includes(user.value.role))
const showPermissionNotice = computed(() => !canOperate.value || route.query.denied === 'Optimization')

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f4f6f8;
  color: #1f2933;
}

.topbar {
  height: 68px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #d8dee6;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  width: 12px;
  height: 28px;
  background: #2457a6;
  display: inline-block;
  border-radius: 2px;
}

.brand strong,
.brand span {
  display: block;
}

.brand strong {
  font-size: 16px;
}

.brand span {
  margin-top: 2px;
  color: #697586;
  font-size: 12px;
}

.nav {
  display: flex;
  gap: 8px;
}

.nav a,
.account button,
.actions a {
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease;
}

.nav a {
  padding: 8px 12px;
  color: #4b5563;
}

.nav a.router-link-active,
.nav a:hover {
  color: #183b70;
  background: #edf2f7;
}

.account {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #52606d;
  font-size: 14px;
}

.role {
  padding: 3px 8px;
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
}

.role.admin { background: #a61b1b; }
.role.operator { background: #2457a6; }
.role.viewer { background: #52606d; }

.username {
  font-weight: 600;
  color: #1f2933;
}

.account button {
  padding: 6px 10px;
  border: 1px solid #cbd2d9;
  background: #fff;
  color: #4b5563;
  cursor: pointer;
}

.account button:hover {
  border-color: #a61b1b;
  color: #a61b1b;
}

.content {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px 32px;
}

.overview {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 380px;
  gap: 28px;
  align-items: stretch;
}

.overview-copy,
.task-panel,
.modules article,
.notice {
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 6px;
}

.overview-copy {
  padding: 40px;
}

.eyebrow {
  color: #52606d;
  font-size: 13px;
}

h1 {
  margin: 12px 0 16px;
  font-size: 34px;
  line-height: 1.25;
  font-weight: 700;
}

.overview-copy p {
  max-width: 680px;
  margin: 0;
  color: #52606d;
  line-height: 1.8;
}

.actions {
  margin-top: 28px;
  display: flex;
  gap: 12px;
}

.actions a {
  padding: 10px 16px;
  border: 1px solid #2457a6;
  font-weight: 600;
}

.actions .primary {
  color: #fff;
  background: #2457a6;
}

.actions .secondary {
  color: #2457a6;
  background: #fff;
}

.task-panel {
  padding: 24px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e7eb;
}

.panel-head span {
  font-size: 15px;
  font-weight: 700;
}

.panel-head strong {
  padding: 3px 8px;
  border-radius: 4px;
  background: #e3f8eb;
  color: #217a3d;
  font-size: 12px;
}

dl {
  margin: 16px 0 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

dt {
  color: #697586;
  font-size: 13px;
}

dd {
  margin: 6px 0 0;
  color: #183b70;
  font-size: 24px;
  font-weight: 700;
}

.modules {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.modules article {
  padding: 22px;
}

.module-index {
  color: #8a94a6;
  font-size: 13px;
  font-weight: 700;
}

.modules h2 {
  margin: 10px 0;
  font-size: 18px;
}

.modules p {
  margin: 0;
  color: #52606d;
  line-height: 1.7;
}

.notice {
  margin-top: 18px;
  padding: 14px 16px;
  color: #8a4b0f;
  background: #fff8e6;
  border-color: #f0c36d;
}

.footer {
  max-width: 1180px;
  margin: 0 auto;
  padding: 18px 24px 28px;
  display: flex;
  justify-content: space-between;
  color: #697586;
  font-size: 13px;
}

@media (max-width: 900px) {
  .topbar,
  .account,
  .nav,
  .actions,
  .footer {
    flex-wrap: wrap;
  }

  .topbar {
    height: auto;
    gap: 14px;
    padding: 16px;
  }

  .overview,
  .modules {
    grid-template-columns: 1fr;
  }

  .overview-copy {
    padding: 28px;
  }
}
</style>
