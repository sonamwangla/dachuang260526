<template>
  <div class="dashboard-container">
    <Header :currentTime="currentTime" @exportReport="handleExport" />

    <main class="main-content">
      <SidebarLeft ref="leftSidebar" />

      <MapContainer
        :mockPoints="mockPoints"
        :historyPoints="historyPoints"
        :heatmapVisible="heatmapVisible"
        :selectedPoint="selectedPoint"
        @selectPoint="handlePointSelect"
        @toggleHeatmap="heatmapVisible = !heatmapVisible"
      />

      <SidebarRight
        ref="rightSidebar"
        :selectedPoint="selectedPoint"
        :analysisResult="analysisResult"
        @action="handleAction"
      />
    </main>

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

const API_BASE = '/api'
const authAxios = axios.create()
authAxios.interceptors.request.use(config => {
  config.headers['x-access-token'] = localStorage.getItem('token')
  return config
})

const mockPoints = ref([
  { id: 101, name: '布达拉宫北侧山谷', lat: 29.66, lng: 91.117, alt: 3720, rsrp: -108, suggestions: ['调整天线下倾角 -5 度', '增加 5G 微基站'] },
  { id: 102, name: '拉萨河滨路段', lat: 29.645, lng: 91.13, alt: 3650, rsrp: -103, suggestions: ['优化邻区干扰', '增加室内分布系统'] },
  { id: 103, name: '纳金路弯区', lat: 29.665, lng: 91.16, alt: 3685, rsrp: -111, suggestions: ['校正基站方位角', '更换高增益天线'] }
])
const historyPoints = ref<any[]>([])
const logs = ref<any[]>([])
const selectedPoint = ref<any>(null)
const analysisResult = ref<any>(null)
const heatmapVisible = ref(true)
const currentTime = ref(new Date().toLocaleTimeString())

const leftSidebar = ref()
const rightSidebar = ref()

const buildFallbackHistory = () => {
  const carriers = ['中国移动', '中国电信', '中国联通']
  const now = Date.now()

  return Array.from({ length: 80 }, (_, index) => {
    const timestamp = new Date(now - index * 45_000)
    const rsrp = -82 - Math.round(Math.random() * 38)

    return {
      id: index + 1,
      lat: Number((29.655 + (Math.random() - 0.5) * 0.052).toFixed(6)),
      lng: Number((91.125 + (Math.random() - 0.5) * 0.084).toFixed(6)),
      alt: Number((3600 + Math.random() * 520).toFixed(1)),
      rsrp,
      sinr: Number((8 + Math.random() * 18).toFixed(1)),
      carrier: carriers[index % carriers.length],
      device_id: `Device-${String(24 + (index % 16)).padStart(3, '0')}`,
      time: timestamp.toLocaleTimeString()
    }
  })
}

const handlePointSelect = async (p: any) => {
  selectedPoint.value = p
  analysisResult.value = null

  try {
    const res = await authAxios.post(`${API_BASE}/analysis/predict`, {
      lat: p.lat,
      lng: p.lng,
      alt: p.alt || 3650
    })
    analysisResult.value = {
      ...res.data,
      environment: { status: (p.alt || 3650) > 4500 ? '极高海拔环境' : '常规高原环境' }
    }
  } catch (err) {
    analysisResult.value = {
      predicted_rsrp: p.rsrp,
      suggestion: '后端分析服务暂不可用，请检查服务状态。',
      environment: { status: '未获取' }
    }
  }
}

const handleAction = () => {
  const u = JSON.parse(localStorage.getItem('user') || '{}')
  if (u.role !== 'admin') {
    alert('权限不足：仅管理员可执行指令下发')
    return
  }
  alert(`指令已下发：${selectedPoint.value?.name || selectedPoint.value?.carrier || '选中区域'}`)
}

const fetchData = async () => {
  try {
    const res = await authAxios.get(`${API_BASE}/history`)
    historyPoints.value = res.data
    logs.value = [...res.data].sort((a, b) => b.id - a.id).slice(0, 200)
  } catch (err) {
    const fallback = buildFallbackHistory()
    historyPoints.value = fallback
    logs.value = fallback
  }
}

const handleExport = () => {
  alert('如需导出 PDF 报告，请进入仿真优化页面生成。')
}

let dataTimer: number | undefined
let clockTimer: number | undefined

const handleResize = () => {
  leftSidebar.value?.resize()
  rightSidebar.value?.resize()
}

onMounted(() => {
  fetchData()
  dataTimer = window.setInterval(fetchData, 8000)
  clockTimer = window.setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (dataTimer) window.clearInterval(dataTimer)
  if (clockTimer) window.clearInterval(clockTimer)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f4f6f8;
  color: #1f2933;
}

.main-content {
  flex: 1;
  display: flex;
  min-height: 0;
  position: relative;
  overflow: hidden;
}
</style>
