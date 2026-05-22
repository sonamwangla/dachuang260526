<template>
  <footer class="footer-log white-footer shadow">
    <div class="log-container-dual">
      
      <!-- 左侧：实时数据流 -->
      <div class="log-column realtime-col">
        <div class="column-header">
          <span class="title"><span class="pulse-dot"></span> 实时采集数据流</span>
          <span class="status-tag">Device-024 Online</span>
        </div>
        <div class="log-content" ref="realtimeContainer">
          <transition-group name="log-list">
            <div v-for="log in realtimeLogs" :key="'rt-'+log.id" class="log-line">
              <span class="log-time">{{ log.time }}</span>
              <span class="log-carrier cmcc">{{ log.carrier }}</span>
              <span class="log-metric">RSRP: <span :class="getRsrpClass(log.rsrp)">{{ log.rsrp }}dBm</span></span>
              <span class="log-coord">({{ log.lat }}, {{ log.lng }})</span>
            </div>
          </transition-group>
        </div>
      </div>

      <!-- 中间分割线 -->
      <div class="column-divider"></div>

      <!-- 右侧：历史存档记录 -->
      <div class="log-column history-col">
        <div class="column-header">
          <span class="title">📜 历史存档记录</span>
          <span class="status-tag gray">Archive Mode</span>
        </div>
        <div class="log-content">
          <div v-for="log in historyLogs" :key="'hi-'+log.id" class="log-line gray-line">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-carrier">{{ log.carrier }}</span>
            <span class="log-metric">RSRP: {{ log.rsrp }}dBm</span>
            <span class="log-device">ID: {{ log.device_id }}</span>
          </div>
        </div>
      </div>

    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'

const props = defineProps<{ logs: any[] }>()

// 逻辑：前 20 条作为“实时”，其余作为“历史”
const realtimeLogs = computed(() => props.logs.slice(0, 20))
const historyLogs = computed(() => props.logs.slice(20))

const getRsrpClass = (val: number) => {
  if (val > -90) return 'green'
  if (val > -105) return 'yellow'
  return 'red'
}
</script>

<style scoped>
.footer-log { height: 200px; background: #ffffff; border-top: 1px solid #e8e8e8; display: flex; }
.log-container-dual { flex: 1; display: flex; overflow: hidden; }

.log-column { flex: 1; display: flex; flex-direction: column; padding: 0 15px; }
.column-header { 
  display: flex; justify-content: space-between; align-items: center; 
  padding: 10px 0; border-bottom: 1px solid #f0f0f0; margin-bottom: 8px;
}
.column-header .title { font-size: 13px; font-weight: bold; color: #001529; display: flex; align-items: center; gap: 8px; }
.status-tag { font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #e6f7ff; color: #1890ff; }
.status-tag.gray { background: #f5f5f5; color: #8c8c8c; }

.log-content { flex: 1; overflow-y: auto; font-family: 'Inter', monospace; font-size: 12px; }
.log-line { display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid #f9f9f9; align-items: center; white-space: nowrap; }
.gray-line { opacity: 0.7; border-bottom-style: dashed; }

.log-time { color: #bfbfbf; width: 70px; }
.log-carrier { width: 60px; font-weight: bold; color: #1890ff; }
.log-metric { width: 100px; }
.log-coord { color: #13c2c2; font-size: 11px; }
.log-device { color: #8c8c8c; font-size: 11px; }

.column-divider { width: 1px; background: #eee; margin: 15px 0; }

.pulse-dot { width: 8px; height: 8px; background: #52c41a; border-radius: 50%; animation: pulse 1.5s infinite; }
.green { color: #52c41a; } .yellow { color: #faad14; } .red { color: #ff4d4f; }

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(82, 196, 26, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(82, 196, 26, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(82, 196, 26, 0); }
}

/* 动画效果 */
.log-list-enter-active { transition: all 0.4s ease; }
.log-list-enter-from { opacity: 0; transform: translateX(-20px); }
</style>
