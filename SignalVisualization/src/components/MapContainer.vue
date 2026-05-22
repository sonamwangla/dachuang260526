<template>
  <section class="center-map">
    <div id="map" class="map-container"></div>

    <div class="map-overlay no-print">
      <div class="carrier-legend">
        <div><span class="dot cmcc"></span> 中国移动</div>
        <div><span class="dot ctc"></span> 中国电信</div>
        <div><span class="dot cuc"></span> 中国联通</div>
        <div><span class="dot danger"></span> 重点优化点</div>
        <div><span class="station-symbol"></span> 模拟基站</div>
      </div>
      <button type="button" @click="$emit('toggleHeatmap')">
        热力图：{{ heatmapVisible ? '开' : '关' }}
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

const props = defineProps<{
  mockPoints: any[]
  historyPoints: any[]
  heatmapVisible: boolean
  selectedPoint: any
}>()

const emit = defineEmits(['selectPoint', 'toggleHeatmap'])
let map: L.Map
let stationLayer: L.LayerGroup
let heatmapLayer: any
let historyLayer: L.LayerGroup
let mockLayer: L.LayerGroup

const allStations = ref<any[]>([])

const getCarrierColor = (carrier: string) => {
  if (carrier?.includes('移动')) return '#2457a6'
  if (carrier?.includes('电信')) return '#217a3d'
  return '#b7791f'
}

const getDistance = (lat1: number, lng1: number, lat2: number, lng2: number) => {
  return Math.sqrt((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2)
}

const initMap = () => {
  map = L.map('map', {
    zoomControl: false,
    attributionControl: false,
    preferCanvas: true
  }).setView([29.655, 91.125], 13)

  const amapLayer = L.tileLayer('http://webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    minZoom: 3,
    maxZoom: 18
  })

  const amapLabels = L.tileLayer('http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    opacity: 0.82
  })

  amapLayer.addTo(map)
  amapLabels.addTo(map)

  historyLayer = L.layerGroup().addTo(map)
  mockLayer = L.layerGroup().addTo(map)
  stationLayer = L.layerGroup().addTo(map)
  heatmapLayer = (L as any).heatLayer([], { radius: 25, blur: 15 }).addTo(map)

  const latMin = 29.626125
  const latMax = 29.692442
  const lngMin = 91.039857
  const lngMax = 91.207659
  const step = 0.007
  const carriers = ['中国移动', '中国电信', '中国联通']
  let stationCount = 1
  allStations.value = []

  for (let lat = latMin; lat <= latMax; lat += step) {
    for (let lng = lngMin; lng <= lngMax; lng += step) {
      const finalLat = lat + (Math.random() - 0.5) * 0.004
      const finalLng = lng + (Math.random() - 0.5) * 0.004
      const stationId = `BS-${stationCount.toString().padStart(3, '0')}`
      const carrier = carriers[Math.floor(Math.random() * carriers.length)]

      allStations.value.push({ id: stationId, lat: finalLat, lng: finalLng, carrier })

      const stationIcon = L.divIcon({
        html: `<div class="bs-marker"><span></span><em>${stationId}</em></div>`,
        className: 'bs-icon-container',
        iconSize: [46, 34],
        iconAnchor: [23, 26]
      })

      L.marker([finalLat, finalLng], { icon: stationIcon })
        .addTo(stationLayer)
        .bindTooltip(`
          <div class="bs-preview-popup">
            <div class="bs-preview-header">
              <strong>${stationId}</strong>
              <span>运行中</span>
            </div>
            <div class="bs-preview-body">
              <p><b>运营商:</b> ${carrier}</p>
              <p><b>经度:</b> ${finalLng.toFixed(6)}</p>
              <p><b>纬度:</b> ${finalLat.toFixed(6)}</p>
            </div>
          </div>
        `, {
          direction: 'top',
          offset: [0, -18],
          className: 'custom-bs-tooltip'
        })

      stationCount++
    }
  }

  props.mockPoints.forEach(point => {
    const marker = L.circleMarker([point.lat, point.lng], {
      radius: 10,
      color: '#b42318',
      fillColor: '#b42318',
      fillOpacity: 0.72,
      weight: 2
    })
    marker.addTo(mockLayer).bindTooltip(`<b>重点优化:</b> ${point.name}`)
    marker.on('click', () => emit('selectPoint', point))
  })
}

const updateData = () => {
  if (!historyLayer || !props.historyPoints) return

  historyLayer.clearLayers()
  const heatData: any[] = []
  const displayPoints = props.historyPoints.slice(-2000)

  props.historyPoints.forEach(point => {
    heatData.push([point.lat, point.lng, (Math.abs(point.rsrp) - 70) / 50])
  })

  displayPoints.forEach(point => {
    const marker = L.circleMarker([point.lat, point.lng], {
      radius: 7,
      color: '#fff',
      weight: 2,
      fillColor: getCarrierColor(point.carrier),
      fillOpacity: 0.9
    })

    marker.addTo(historyLayer)
    marker.on('mouseover', (event: any) => {
      let nearestBS = { id: '未知', dist: Infinity }
      allStations.value.forEach(station => {
        const distance = getDistance(point.lat, point.lng, station.lat, station.lng)
        if (distance < nearestBS.dist) {
          nearestBS = { id: station.id, dist: distance }
        }
      })

      const distInMeters = (nearestBS.dist * 111000).toFixed(0)
      event.target.bindTooltip(`
        <div class="signal-tooltip">
          <div class="signal-header" style="color: ${getCarrierColor(point.carrier)}">
            <b>${point.carrier}</b>
          </div>
          <div class="signal-body">
            <p>强度: <b>${point.rsrp} dBm</b></p>
            <p>连接基站: <b>${nearestBS.id}</b></p>
            <p>距离基站: ~${distInMeters}m</p>
          </div>
        </div>
      `, { className: 'custom-signal-tooltip' }).openTooltip()
    })
  })

  heatmapLayer.setLatLngs(heatData)
}

watch(() => props.historyPoints.length, updateData)
watch(() => props.heatmapVisible, value => {
  if (!map || !heatmapLayer) return
  if (value) map.addLayer(heatmapLayer)
  else map.removeLayer(heatmapLayer)
})

onMounted(() => {
  initMap()
  updateData()
})
</script>

<style scoped>
.center-map {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
  background: #dfe5ec;
}

.map-overlay {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.carrier-legend {
  padding: 12px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #d8dee6;
  border-radius: 6px;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.12);
}

.carrier-legend div {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  color: #344054;
  font-size: 12px;
}

.carrier-legend div:last-child {
  margin-bottom: 0;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.station-symbol {
  width: 10px;
  height: 10px;
  border: 2px solid #2457a6;
  display: inline-block;
  box-sizing: border-box;
}

.cmcc { background: #2457a6; }
.ctc { background: #217a3d; }
.cuc { background: #b7791f; }
.danger { background: #b42318; }

button {
  padding: 8px 12px;
  border: 1px solid #2457a6;
  border-radius: 4px;
  background: #2457a6;
  color: #fff;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
}

:deep(.bs-marker) {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

:deep(.bs-marker span) {
  width: 14px;
  height: 14px;
  display: block;
  background: #fff;
  border: 3px solid #2457a6;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.3);
}

:deep(.bs-marker em) {
  padding: 1px 4px;
  background: rgba(15, 23, 42, 0.72);
  color: #fff;
  border-radius: 3px;
  font-size: 10px;
  font-style: normal;
  white-space: nowrap;
}

:deep(.custom-bs-tooltip),
:deep(.custom-signal-tooltip) {
  padding: 0;
  overflow: hidden;
  border: 0;
  border-radius: 6px;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.18);
}

:deep(.bs-preview-popup) {
  min-width: 150px;
}

:deep(.bs-preview-header) {
  padding: 6px 9px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  background: #edf2f7;
  border-bottom: 1px solid #d8dee6;
}

:deep(.bs-preview-header span) {
  color: #217a3d;
  font-size: 11px;
}

:deep(.bs-preview-body),
:deep(.signal-tooltip) {
  padding: 8px 9px;
  color: #344054;
  font-size: 12px;
}

:deep(.bs-preview-body p),
:deep(.signal-tooltip p) {
  margin: 4px 0;
}
</style>
