<template>
  <footer class="footer-log">
    <div class="log-column">
      <div class="column-header">
        <span>实时采集数据</span>
        <strong>Device-024 Online</strong>
      </div>
      <div class="log-content">
        <div v-for="log in realtimeLogs" :key="'rt-' + log.id" class="log-line">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-carrier">{{ log.carrier }}</span>
          <span>RSRP: <b :class="getRsrpClass(log.rsrp)">{{ log.rsrp }} dBm</b></span>
          <span class="log-coord">({{ log.lat }}, {{ log.lng }})</span>
        </div>
      </div>
    </div>

    <div class="log-column">
      <div class="column-header">
        <span>历史存档记录</span>
        <strong class="muted">Archive</strong>
      </div>
      <div class="log-content">
        <div v-for="log in historyLogs" :key="'hi-' + log.id" class="log-line archived">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-carrier">{{ log.carrier }}</span>
          <span>RSRP: {{ log.rsrp }} dBm</span>
          <span class="log-device">ID: {{ log.device_id }}</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ logs: any[] }>()

const realtimeLogs = computed(() => props.logs.slice(0, 20))
const historyLogs = computed(() => props.logs.slice(20))

const getRsrpClass = (val: number) => {
  if (val > -90) return 'green'
  if (val > -105) return 'yellow'
  return 'red'
}
</script>

<style scoped>
.footer-log {
  height: 190px;
  flex-shrink: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: #fff;
  border-top: 1px solid #d8dee6;
}

.log-column {
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 0 14px;
}

.log-column + .log-column {
  border-left: 1px solid #e4e7eb;
}

.column-header {
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e4e7eb;
  color: #1f2933;
  font-size: 13px;
  font-weight: 700;
}

.column-header strong {
  padding: 2px 6px;
  border-radius: 4px;
  background: #e3f8eb;
  color: #217a3d;
  font-size: 11px;
}

.column-header .muted {
  background: #edf2f7;
  color: #697586;
}

.log-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 12px;
}

.log-content::-webkit-scrollbar {
  width: 6px;
}

.log-content::-webkit-scrollbar-thumb {
  background: #cbd2d9;
  border-radius: 3px;
}

.log-content::-webkit-scrollbar-track {
  background: transparent;
}

.log-line {
  display: grid;
  grid-template-columns: 70px 76px 120px minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #f1f3f5;
  white-space: nowrap;
}

.archived {
  color: #697586;
}

.log-time,
.log-device {
  color: #8a94a6;
}

.log-carrier {
  color: #2457a6;
  font-weight: 700;
}

.log-coord {
  color: #52606d;
  overflow: hidden;
  text-overflow: ellipsis;
}

.green { color: #217a3d; }
.yellow { color: #b7791f; }
.red { color: #b42318; }
</style>
