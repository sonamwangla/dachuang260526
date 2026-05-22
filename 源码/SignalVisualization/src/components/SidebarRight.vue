<template>
  <aside class="sidebar right-sidebar glass-panel">
    <div class="card white-card shadow">
      <div class="card-title">
        <span class="title-icon">🕸️</span>
        <h3>信号环境影响因子</h3>
      </div>
      <div ref="radarChart" class="chart-box"></div>
    </div>
    <div class="card optimization-panel white-card shadow">
      <div class="card-title">
        <span class="title-icon">💡</span>
        <h3>智能优化建议</h3>
      </div>
      <div v-if="selectedPoint" class="opt-content">
        <div class="selected-info">
          <div class="info-row"><strong>区域:</strong> {{ selectedPoint.name }}</div>
          <div class="info-row">
            <strong>当前 RSRP:</strong> 
            <span :class="getRsrpClass(selectedPoint.rsrp)">{{ selectedPoint.rsrp }} dBm</span>
          </div>
          
          <div v-if="analysisResult" class="ai-analysis">
            <div class="divider">AI 模型预测分析</div>
            <div class="info-row">
              <strong>预测 RSRP:</strong> 
              <span class="predicted">{{ analysisResult.predicted_rsrp }} dBm</span>
            </div>
            <div class="info-row">
              <strong>海拔状态:</strong> 
              <span>{{ analysisResult.environment.status }}</span>
            </div>
          </div>
          <div v-else class="loading-ai">正在调用 AI 模型分析...</div>
        </div>

        <div class="suggest-box">
          <h4>优化策略:</h4>
          <ul>
            <li v-if="analysisResult">
              <span class="bullet">⚡</span> {{ analysisResult.suggestion }}
            </li>
            <li v-for="(sug, idx) in selectedPoint.suggestions" :key="idx">
              <span class="bullet">▶</span> {{ sug }}
            </li>
          </ul>
        </div>
        <button class="btn-action pulse-btn" @click="$emit('action')">下发优化指令</button>
      </div>
      <div v-else class="empty-hint">
        <div class="scan-animation"></div>
        <span>点击地图弱信号点查看 AI 深度分析</span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, defineExpose } from 'vue'
import * as echarts from 'echarts'

defineProps<{ 
  selectedPoint: any,
  analysisResult: any
}>()
defineEmits(['action'])

const radarChart = ref<HTMLElement>()
let chart3: echarts.EChartsType

const getRsrpClass = (val: number) => {
  if (val > -90) return 'green'
  if (val > -105) return 'yellow'
  return 'red'
}

const initCharts = () => {
  chart3 = echarts.init(radarChart.value!)
  chart3.setOption({
    radar: {
      indicator: [
        { name: '海拔影响', max: 100 },
        { name: '地形遮挡', max: 100 },
        { name: '建筑物穿透', max: 100 },
        { name: '多径干扰', max: 100 },
        { name: '气象损耗', max: 100 }
      ],
      shape: 'circle',
      axisName: { color: '#595959', fontSize: 10 },
      splitArea: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0' } },
      axisLine: { lineStyle: { color: '#f0f0f0' } }
    },
    series: [{
      type: 'radar',
      data: [{ value: [85, 70, 90, 60, 45], name: '当前区域', areaStyle: { color: 'rgba(24, 144, 255, 0.1)' }, lineStyle: { color: '#1890ff', width: 2 }, symbol: 'none' }]
    }]
  })
}

const resize = () => {
  chart3?.resize()
}

onMounted(() => {
  initCharts()
})

defineExpose({ resize })
</script>

<style scoped>
.sidebar { 
  width: 360px; padding: 20px; display: flex; flex-direction: column; gap: 20px; z-index: 10;
  height: 100%; overflow-y: auto; box-sizing: border-box;
}
/* 美化科技感滚动条 */
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: rgba(24, 144, 255, 0.4); border-radius: 10px; }
.sidebar::-webkit-scrollbar-thumb:hover { background: #1890ff; }

.card {
  background: #ffffff; border: 1px solid #f0f0f0; border-radius: 12px;
  padding: 15px; flex-shrink: 0; display: flex; flex-direction: column;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.card-title { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid #f9f9f9; padding-bottom: 8px; }
.card h3 { font-size: 1.1rem; margin: 0; color: #001529; font-weight: bold; }
.chart-box { flex: 1; width: 100%; min-height: 180px; }

.ai-analysis { margin-top: 15px; padding: 10px; background: #e6f7ff; border-radius: 8px; }
.divider { font-size: 11px; color: #1890ff; text-align: center; margin-bottom: 8px; border-bottom: 1px solid rgba(24, 144, 255, 0.2); }
.predicted { color: #13c2c2; font-weight: bold; }
.loading-ai { font-size: 12px; color: #8c8c8c; font-style: italic; margin-top: 10px; }

.green { color: #52c41a; }
.yellow { color: #faad14; }
.red { color: #ff4d4f; }

.opt-content { animation: fadeIn 0.5s ease-out; }
.selected-info { font-size: 14px; margin-bottom: 15px; color: #595959; }
.suggest-box { background: #fff1f0; border-left: 3px solid #ff4d4f; padding: 12px; border-radius: 0 4px 4px 0; margin: 15px 0; }
.suggest-box h4 { margin: 0 0 10px 0; font-size: 14px; color: #ff4d4f; }
.suggest-box ul { list-style: none; padding: 0; margin: 0; }
.suggest-box li { margin-bottom: 8px; font-size: 13px; display: flex; gap: 8px; color: #595959; }
.bullet { color: #ff4d4f; font-size: 10px; }

.btn-action {
  width: 100%; background: #ff4d4f; color: #fff; border: none; padding: 12px; border-radius: 6px;
  cursor: pointer; font-weight: bold; transition: all 0.3s; margin-top: 15px; box-shadow: 0 4px 12px rgba(255, 77, 79, 0.3);
}
.btn-action:hover { background: #ff7875; transform: translateY(-2px); }

.empty-hint { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #bfbfbf; gap: 20px; }
.scan-animation { width: 60px; height: 60px; border: 2px solid #1890ff; border-radius: 50%; position: relative; animation: scan 3s infinite linear; opacity: 0.3; }
.scan-animation::after { content: ''; position: absolute; top: 50%; left: 50%; width: 50%; height: 2px; background: #1890ff; transform-origin: left center; }
@keyframes scan { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
