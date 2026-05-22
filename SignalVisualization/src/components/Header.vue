<template>
  <header class="header">
    <div class="header-left">
      <router-link to="/" class="home-link">系统概览</router-link>
      <span class="separator"></span>
      <h1>西藏高原移动信号监控大屏</h1>
      <div class="live-stats">
        <span>平均海拔 3650m</span>
        <span class="online">24/30 设备在线</span>
      </div>
    </div>

    <div class="header-right">
      <router-link to="/optimization" class="nav-link">仿真优化</router-link>
      <button type="button" @click="$emit('exportReport')">导出报告</button>
      <time>{{ currentTime }}</time>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{ currentTime: string }>()
defineEmits(['exportReport'])
</script>

<style scoped>
.header {
  height: 62px;
  padding: 0 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  background: #fff;
  border-bottom: 1px solid #d8dee6;
  z-index: 1000;
}

.header-left,
.header-right,
.live-stats {
  display: flex;
  align-items: center;
}

.header-left {
  gap: 14px;
}

.header-right {
  gap: 12px;
}

.separator {
  width: 1px;
  height: 20px;
  background: #d8dee6;
}

h1 {
  margin: 0;
  color: #1f2933;
  font-size: 18px;
  font-weight: 700;
}

.home-link,
.nav-link {
  color: #4b5563;
  text-decoration: none;
  font-size: 14px;
}

.home-link:hover,
.nav-link:hover {
  color: #2457a6;
}

.live-stats {
  gap: 10px;
  color: #697586;
  font-size: 13px;
}

.online {
  color: #217a3d;
}

button {
  padding: 8px 12px;
  border: 1px solid #2457a6;
  border-radius: 4px;
  background: #2457a6;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
}

time {
  min-width: 78px;
  color: #183b70;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 17px;
  font-weight: 700;
  text-align: right;
}

@media (max-width: 980px) {
  .live-stats {
    display: none;
  }
}
</style>
