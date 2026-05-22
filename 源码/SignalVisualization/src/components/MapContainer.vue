<template>
  <section class="center-map">
    <div id="map" class="map-container"></div>
    
    <div class="map-overlay no-print">
      <div class="carrier-legend">
        <div class="legend-item"><span class="dot cmcc"></span> 移动</div>
        <div class="legend-item"><span class="dot ctc"></span> 电信</div>
        <div class="legend-item"><span class="dot cuc"></span> 联通</div>
        <div class="legend-item"><span class="dot danger"></span> 重点优化点</div>
        <div class="legend-item"><span class="icon-bs">🗼</span> 模拟基站</div>
      </div>
      <button @click="$emit('toggleHeatmap')" class="btn-tool">🔥 热力图: {{ heatmapVisible ? '开' : '关' }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

const props = defineProps<{
  mockPoints: any[],
  historyPoints: any[],
  heatmapVisible: boolean,
  selectedPoint: any
}>()

const emit = defineEmits(['selectPoint', 'toggleHeatmap'])
let map: L.Map
let stationLayer: L.LayerGroup
let heatmapLayer: any
let historyLayer: L.LayerGroup
let mockLayer: L.LayerGroup

// 存储基站数据用于计算就近连接
const allStations = ref<any[]>([])

const getCarrierColor = (c: string) => {
  if (c.includes('移动')) return '#1890ff'
  if (c.includes('电信')) return '#52c41a'
  return '#fa8c16'
}

// 计算两点间的距离 (简易欧氏距离，适用于小范围)
const getDistance = (lat1: number, lng1: number, lat2: number, lng2: number) => {
  return Math.sqrt(Math.pow(lat1 - lat2, 2) + Math.pow(lng1 - lng2, 2))
}

const initMap = () => {
  map = L.map('map', { 
    zoomControl: false, 
    attributionControl: false, 
    preferCanvas: true 
  }).setView([29.655, 91.125], 13)
  
  // 使用高德卫星混合地图 (卫星图 + 路网)
  const amapLayer = L.tileLayer('http://webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    minZoom: 3,
    maxZoom: 18
  })
  
  const amapLabels = L.tileLayer('http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    opacity: 0.8
  })

  amapLayer.addTo(map)
  amapLabels.addTo(map)
  
  historyLayer = L.layerGroup().addTo(map)
  mockLayer = L.layerGroup().addTo(map)
  stationLayer = L.layerGroup().addTo(map)
  heatmapLayer = (L as any).heatLayer([], { radius: 25, blur: 15 }).addTo(map)

  // --- 模拟基站生成逻辑 (引入随机抖动，使其分布自然) ---
  const latMin = 29.626125; const latMax = 29.692442
  const lngMin = 91.039857; const lngMax = 91.207659
  const step = 0.007 // 约 700m 步长，增加抖动空间

  const carriers = ['中国移动', '中国电信', '中国联通']
  let stationCount = 1
  allStations.value = [] // 重置基站数据

  for (let lat = latMin; lat <= latMax; lat += step) {
    for (let lng = lngMin; lng <= lngMax; lng += step) {
      // 引入约 150-200 米的随机抖动
      const jitterLat = (Math.random() - 0.5) * 0.004
      const jitterLng = (Math.random() - 0.5) * 0.004
      
      const finalLat = lat + jitterLat
      const finalLng = lng + jitterLng
      const stationId = `BS-${stationCount.toString().padStart(3, '0')}`
      const carrier = carriers[Math.floor(Math.random() * carriers.length)]

      // 存入数组供后续计算
      allStations.value.push({ id: stationId, lat: finalLat, lng: finalLng, carrier })
      
      const stationIcon = L.divIcon({
        html: `<div class="bs-marker-wrapper">
                <div class="bs-icon-emoji">🗼</div>
                <div class="bs-id-label">${stationId}</div>
               </div>`,
        className: 'bs-icon-container',
        iconSize: [40, 40],
        iconAnchor: [20, 30]
      })

      L.marker([finalLat, finalLng], { icon: stationIcon })
        .addTo(stationLayer)
        .bindTooltip(`
          <div class="bs-preview-popup">
            <div class="bs-preview-header">
              <span class="bs-preview-id">${stationId}</span>
              <span class="bs-preview-status running">● 运行中</span>
            </div>
            <div class="bs-preview-body">
              <p><b>运营商:</b> ${carrier}</p>
              <p><b>经度:</b> ${finalLng.toFixed(6)}</p>
              <p><b>纬度:</b> ${finalLat.toFixed(6)}</p>
            </div>
          </div>
        `, {
          direction: 'top',
          offset: [0, -20],
          className: 'custom-bs-tooltip'
        })
      
      stationCount++
    }
  }

  // 绘制初始 Mock 点（红色闪烁点）
  props.mockPoints.forEach(p => {
    const m = L.circleMarker([p.lat, p.lng], { radius: 12, color: '#ff4d4f', fillColor: '#ff4d4f', fillOpacity: 0.6, weight: 2 })
    m.addTo(mockLayer).bindTooltip(`<b>重点优化: ${p.name}</b>`)
    m.on('click', () => emit('selectPoint', p))
  })
}

const updateData = () => {
  if (!historyLayer || !props.historyPoints) return
  historyLayer.clearLayers()
  const heatData: any[] = []

  // 限制地图上渲染的圆点数量（例如最多 500 个最亮的点）以保证流畅，热力图仍使用全量数据
  const displayPoints = props.historyPoints.slice(-2000)

  props.historyPoints.forEach(p => {
    heatData.push([p.lat, p.lng, (Math.abs(p.rsrp)-70)/50])
  })

  displayPoints.forEach(p => {
    const marker = L.circleMarker([p.lat, p.lng], { 
      radius: 8, 
      color: '#fff', 
      weight: 2, 
      fillColor: getCarrierColor(p.carrier), 
      fillOpacity: 0.9 
    })
    
    marker.addTo(historyLayer)
    
    // 性能优化：在 addTooltip 时动态生成内容（Leaflet 默认支持动态 HTML）
    marker.on('mouseover', (e: any) => {
      // 只有在鼠标悬停时才计算最近基站，避免每帧都算
      let nearestBS = { id: '未知', dist: Infinity }
      allStations.value.forEach(bs => {
        const d = getDistance(p.lat, p.lng, bs.lat, bs.lng)
        if (d < nearestBS.dist) {
          nearestBS = { id: bs.id, dist: d }
        }
      })
      const distInMeters = (nearestBS.dist * 111000).toFixed(0)

      e.target.bindTooltip(`
        <div class="signal-tooltip">
          <div class="signal-header" style="color: ${getCarrierColor(p.carrier)}">
            <b>${p.carrier}</b>
          </div>
          <div class="signal-body">
            <p>强度: <b>${p.rsrp} dBm</b></p>
            <p style="margin-top: 4px; border-top: 1px dashed #ddd; padding-top: 4px;">
              🔗 已连接: <span style="color: #1d39c4; font-weight: bold;">${nearestBS.id}</span>
            </p>
            <p>距离基站: ~${distInMeters}m</p>
          </div>
        </div>
      `, { className: 'custom-signal-tooltip' }).openTooltip()
    })
  })
  heatmapLayer.setLatLngs(heatData)
}

watch(() => props.historyPoints.length, updateData)
watch(() => props.heatmapVisible, (v) => v ? map.addLayer(heatmapLayer) : map.removeLayer(heatmapLayer))

onMounted(() => {
  initMap()
  updateData()
})
</script>

<style scoped>
.center-map { width: 100%; height: 100%; position: relative; }
.map-container { width: 100%; height: 100%; background: #001529; }
.map-overlay { position: absolute; top: 20px; left: 20px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
.carrier-legend { background: rgba(255,255,255,0.9); padding: 12px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 5px; color: #333; }
.dot { width: 8px; height: 8px; border-radius: 50%; }
.icon-bs { font-size: 16px; margin-right: 4px; }
.cmcc { background: #1890ff; } .ctc { background: #52c41a; } .cuc { background: #fa8c16; } .danger { background: #ff4d4f; }
.btn-tool { background: #1890ff; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold; }

/* 基站 Marker 样式 */
:deep(.bs-marker-wrapper) {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s;
}
:deep(.bs-marker-wrapper:hover) {
  transform: scale(1.2);
}
:deep(.bs-icon-emoji) {
  font-size: 24px;
  filter: drop-shadow(0 0 3px rgba(0,0,0,0.5));
}
:deep(.bs-id-label) {
  font-size: 10px;
  background: rgba(0,0,0,0.6);
  color: white;
  padding: 0 4px;
  border-radius: 4px;
  margin-top: -4px;
  white-space: nowrap;
}

/* Tooltip 预览样式 */
:deep(.custom-bs-tooltip) {
  background: white;
  border: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  padding: 0;
  border-radius: 8px;
  overflow: hidden;
}
:deep(.bs-preview-popup) {
  min-width: 150px;
}
:deep(.bs-preview-header) {
  background: #f0f5ff;
  padding: 6px 10px;
  border-bottom: 1px solid #adc6ff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
:deep(.bs-preview-id) {
  font-weight: bold;
  color: #1d39c4;
}
:deep(.bs-preview-status.running) {
  color: #52c41a;
  font-size: 11px;
}
:deep(.bs-preview-body) {
  padding: 8px 10px;
  font-size: 12px;
}
:deep(.bs-preview-body p) {
  margin: 4px 0;
  color: #555;
}
</style>
