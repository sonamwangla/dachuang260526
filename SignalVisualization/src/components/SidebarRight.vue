<template>
  <aside class="sidebar right-sidebar">
    <section class="card">
      <h3>环境影响因子</h3>
      <div ref="radarChart" class="chart-box"></div>
    </section>

    <section class="card optimization-panel">
      <h3>优化建议</h3>

      <div v-if="selectedPoint" class="opt-content">
        <div class="selected-info">
          <div><strong>区域</strong><span>{{ selectedPoint.name || selectedPoint.carrier }}</span></div>
          <div>
            <strong>当前 RSRP</strong>
            <span :class="getRsrpClass(selectedPoint.rsrp)">{{ selectedPoint.rsrp || '-' }} dBm</span>
          </div>
        </div>

        <div v-if="analysisResult" class="analysis">
          <div><strong>预测 RSRP</strong><span>{{ analysisResult.predicted_rsrp }} dBm</span></div>
          <div><strong>海拔状态</strong><span>{{ analysisResult.environment?.status || '-' }}</span></div>
        </div>
        <div v-else class="loading">正在获取模型分析结果...</div>

        <div class="suggest-box">
          <h4>建议项</h4>
          <ul>
            <li v-if="analysisResult">{{ analysisResult.suggestion }}</li>
            <li v-for="(sug, idx) in selectedPoint.suggestions" :key="idx">{{ sug }}</li>
          </ul>
        </div>

        <button type="button" @click="$emit('action')">下发优化指令</button>
      </div>

      <div v-else class="empty-hint">
        点击地图中的弱覆盖点，查看模型分析和处置建议。
      </div>
    </section>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

defineProps<{
  selectedPoint: any
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
        { name: '建筑穿透', max: 100 },
        { name: '多径干扰', max: 100 },
        { name: '气象损耗', max: 100 }
      ],
      shape: 'circle',
      axisName: { color: '#52606d', fontSize: 10 },
      splitArea: { show: false },
      splitLine: { lineStyle: { color: '#e4e7eb' } },
      axisLine: { lineStyle: { color: '#e4e7eb' } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [85, 70, 90, 60, 45],
        name: '当前区域',
        areaStyle: { color: 'rgba(36, 87, 166, 0.14)' },
        lineStyle: { color: '#2457a6', width: 2 },
        symbol: 'none'
      }]
    }]
  })
}

const resize = () => {
  chart3?.resize()
}

onMounted(initCharts)

defineExpose({ resize })
</script>

<style scoped>
.sidebar {
  width: 340px;
  height: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow-y: auto;
  box-sizing: border-box;
  background: #f8fafc;
  border-left: 1px solid #d8dee6;
}

.card {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  padding: 14px;
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 6px;
}

h3 {
  margin: 0 0 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7eb;
  color: #1f2933;
  font-size: 15px;
}

.chart-box {
  width: 100%;
  min-height: 200px;
}

.selected-info,
.analysis {
  display: grid;
  gap: 8px;
  color: #52606d;
  font-size: 14px;
}

.selected-info div,
.analysis div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.selected-info strong,
.analysis strong {
  color: #344054;
}

.analysis {
  margin-top: 14px;
  padding: 12px;
  background: #f8fafc;
  border: 1px solid #e4e7eb;
  border-radius: 4px;
}

.loading,
.empty-hint {
  color: #697586;
  line-height: 1.7;
  font-size: 14px;
}

.suggest-box {
  margin-top: 14px;
  padding: 12px;
  border-left: 3px solid #b42318;
  background: #fff7f7;
}

h4 {
  margin: 0 0 8px;
  color: #8f1d1d;
  font-size: 14px;
}

ul {
  margin: 0;
  padding-left: 18px;
  color: #52606d;
  line-height: 1.7;
  font-size: 13px;
}

button {
  width: 100%;
  margin-top: 14px;
  padding: 10px 12px;
  border: 1px solid #b42318;
  border-radius: 4px;
  background: #b42318;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
}

.green { color: #217a3d; }
.yellow { color: #b7791f; }
.red { color: #b42318; }
</style>
