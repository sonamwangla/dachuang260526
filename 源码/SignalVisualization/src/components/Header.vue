<template>
  <header class="header white-header">
    <div class="header-left">
      <router-link to="/" class="home-link">🏠 首页</router-link>
      <div class="logo-pulse"></div>
      <h1 class="header-title">西藏高原移动信号监控大屏</h1>
      <div class="live-stats">
        <span class="stat-item"><i class="icon">🏔️</i> 3650m</span>
        <span class="stat-item online"><i class="icon-pulse"></i> 24/30 活跃</span>
      </div>
    </div>
    <div class="header-right">
      <router-link to="/optimization" class="nav-btn">AI 优化中心</router-link>
      <button class="btn-report glow-btn" @click="$emit('exportReport')">导出分析报告</button>
      <div class="digital-clock">{{ currentTime }}</div>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{ currentTime: string }>()
defineEmits(['exportReport'])
</script>

<style scoped>
.header {
  height: 70px; background: #ffffff; display: flex; justify-content: space-between; align-items: center;
  padding: 0 25px; border-bottom: 2px solid #1890ff; box-shadow: 0 2px 10px rgba(0,0,0,0.05); z-index: 1000;
}
.header-left, .header-right { display: flex; align-items: center; gap: 25px; }
.home-link, .nav-btn {
  color: #595959; text-decoration: none; font-size: 0.95rem; font-weight: 500; transition: all 0.3s;
}
.home-link:hover, .nav-btn:hover { color: #1890ff; }
.logo-pulse {
  width: 10px; height: 10px; background: #1890ff; border-radius: 50%; box-shadow: 0 0 10px rgba(24, 144, 255, 0.4);
}
.header-title { font-size: 1.4rem; margin: 0; color: #001529; font-weight: 800; letter-spacing: -0.5px; }
.live-stats { display: flex; gap: 15px; font-size: 0.9rem; color: #8c8c8c; }
.icon-pulse { width: 8px; height: 8px; background: #52c41a; border-radius: 50%; }

.digital-clock { font-family: 'Inter', monospace; font-size: 1.3rem; color: #1890ff; font-weight: bold; }
.glow-btn {
  background: #1890ff; color: #fff; border: none; padding: 10px 22px; border-radius: 6px;
  cursor: pointer; font-weight: bold; box-shadow: 0 4px 10px rgba(24, 144, 255, 0.3);
}
.glow-btn:hover { background: #40a9ff; transform: translateY(-2px); }
</style>
