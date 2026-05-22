<template>
  <div class="dashboard-container">
    <Header :currentTime="currentTime" @exportReport="handleExport" />

    <main class="main-content">
      <!-- 1. 左侧统计图表栏 (ECharts) -->
      <SidebarLeft ref="leftSidebar" />

      <!-- 2. 核心地图区 (Leaflet + Canvas) -->
      <MapContainer 
        :mockPoints="mockPoints"
        :historyPoints="historyPoints"
        :heatmapVisible="heatmapVisible"
        :selectedPoint="selectedPoint"
        @selectPoint="handlePointSelect"
        @toggleHeatmap="heatmapVisible = !heatmapVisible"
      />

      <!-- 3. 右侧 AI 分析栏 (Radar + Suggestions) -->
      <SidebarRight 
        ref="rightSidebar"
        :selectedPoint="selectedPoint"
        :analysisResult="analysisResult"
        @action="handleAction"
      />
    </main>

    <!-- 4. 底部双栏实时/历史日志流 -->
    <FooterLog :logs="logs" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import Header from '../components/Header.vue'
import SidebarLeft from '../components/SidebarLeft.vue'
import MapContainer from '../components/MapContainer.vue'
import SidebarRight from '../components/SidebarRight.vue'
import FooterLog from '../components/FooterLog.vue'

const API_BASE = 'http://127.0.0.1:5000/api'
const authAxios = axios.create()
authAxios.interceptors.request.use(config => {
  config.headers['x-access-token'] = localStorage.getItem('token')
  return config
})

// --- 状态恢复 ---
const mockPoints = ref([
  { id: 101, name: '布达拉宫北侧山谷', lat: 29.660, lng: 91.117, suggestions: ['调整天线俯仰角 -5°', '增加 5G 微基站'] },
  { id: 102, name: '拉萨河滨路段', lat: 29.645, lng: 91.130, suggestions: ['优化邻区干扰', '增加室内分布系统'] },
  { id: 103, name: '纳金路盲区', lat: 29.665, lng: 91.160, suggestions: ['基站位置纠偏', '更换高增益天线'] }
])
const historyPoints = ref<any[]>([])
const logs = ref<any[]>([])
const selectedPoint = ref<any>(null)
const analysisResult = ref<any>(null)
const heatmapVisible = ref(true)
const currentTime = ref(new Date().toLocaleTimeString())

const leftSidebar = ref()
const rightSidebar = ref()

// --- 逻辑恢复 ---
const handlePointSelect = async (p: any) => {
  selectedPoint.value = p
  analysisResult.value = null 
  try {
    const res = await authAxios.post(`${API_BASE}/analysis/predict`, { lat: p.lat, lng: p.lng, alt: p.alt || 3650 })
    // 为 SidebarRight 补全所需的环境状态结构
    analysisResult.value = {
      ...res.data,
      environment: { status: p.alt > 4500 ? '极高海拔环境' : '正常高原环境' }
    }
  } catch (err) {}
}

const handleAction = () => {
  const u = JSON.parse(localStorage.getItem('user') || '{}')
  if (u.role !== 'admin') return alert('权限不足：仅管理员可执行下发指令')
  alert(`【指令已下发】正在远程优化区域: ${selectedPoint.value.name || selectedPoint.value.carrier}`)
}

const fetchData = async () => {
  try {
    const res = await authAxios.get(`${API_BASE}/history`)
    historyPoints.value = res.data
    // 关键修复：日志流切片保护性能，增加上限到 200 条
    logs.value = [...res.data].sort((a,b) => b.id - a.id).slice(0, 200)
  } catch (err) {}
}

const handleExport = () => alert('报告生成中，请在仿真中心导出专业 PDF 版本')

let timer: any;
onMounted(() => {
  fetchData()
  timer = setInterval(fetchData, 8000)
  const clock = setInterval(() => currentTime.value = new Date().toLocaleTimeString(), 1000)
  
  window.addEventListener('resize', () => {
    leftSidebar.value?.resize(); rightSidebar.value?.resize()
  })
  onUnmounted(() => { clearInterval(timer); clearInterval(clock) })
})
</script>

<style>
body { margin: 0; padding: 0; overflow: hidden; background: #ffffff; }
.dashboard-container {
  width: 100vw; height: 100vh; background: #ffffff;
  display: flex; flex-direction: column; color: #333; font-family: 'Inter', sans-serif;
}
.main-content { flex: 1; display: flex; position: relative; overflow: hidden; }

/* 深度美化侧边栏容器 */
:deep(.left-sidebar), :deep(.right-sidebar) {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid #e8e8e8;
  box-shadow: 0 0 30px rgba(0,0,0,0.1);
  z-index: 10;
  transition: 0.3s;
}

:deep(.left-sidebar:hover), :deep(.right-sidebar:hover) {
  border-color: #1890ff;
}

/* 隐藏 Leaflet 的默认白色边框 */
:deep(.leaflet-container) {
  background: #f5f5f5 !important;
}
</style>
