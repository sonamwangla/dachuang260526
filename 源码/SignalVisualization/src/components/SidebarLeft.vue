<template>
  <aside class="sidebar left-sidebar glass-panel">
    <div class="card white-card">
      <div class="card-title">
        <span class="title-icon">📊</span>
        <h3>运营商覆盖质量对比 (RSRP)</h3>
      </div>
      <div ref="rsrpChart" class="chart-box"></div>
    </div>
    <div class="card white-card">
      <div class="card-title">
        <span class="title-icon">📉</span>
        <h3>海拔-信号衰减回归分析</h3>
      </div>
      <div ref="attenuationChart" class="chart-box"></div>
    </div>
    <div class="card white-card statistics-card">
      <div class="card-title">
        <span class="title-icon">📈</span>
        <h3>区域实时信号状态统计</h3>
      </div>
      <ul class="stat-list">
        <li class="stat-row">
          <span class="label">良好 (>-90dBm):</span>
          <div class="progress-bar"><div class="progress-fill green" style="width: 65%"></div></div>
          <span class="val green">65%</span>
        </li>
        <li class="stat-row">
          <span class="label">一般 (-105~-90dBm):</span>
          <div class="progress-bar"><div class="progress-fill yellow" style="width: 22%"></div></div>
          <span class="val yellow">22%</span>
        </li>
        <li class="stat-row">
          <span class="label">极弱 (<-105dBm):</span>
          <div class="progress-bar"><div class="progress-fill red" style="width: 13%"></div></div>
          <span class="val red">13%</span>
        </li>
      </ul>
    </div>
    <!-- 强力占位块：确保滚动到底部后，内容上方有足够留白，绝对不会被页脚遮挡 -->
    <div class="bottom-spacer"></div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, defineExpose } from 'vue'
import * as echarts from 'echarts'

const rsrpChart = ref<HTMLElement>()
const attenuationChart = ref<HTMLElement>()

let chart1: echarts.EChartsType
let chart2: echarts.EChartsType

const initCharts = () => {
  chart1 = echarts.init(rsrpChart.value!)
  chart1.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: { top: 0 },
    grid: { left: '3%', right: '4%', bottom: '5%', containLabel: true },
    xAxis: { type: 'category', data: ['拉萨', '日喀则', '昌都', '林芝'] },
    yAxis: { type: 'value' },
    series: [
      { name: '中国移动', type: 'bar', data: [-85, -92, -88, -95], itemStyle: { color: '#1890ff' } },
      { name: '中国电信', type: 'bar', data: [-88, -95, -90, -92], itemStyle: { color: '#52c41a' } },
      { name: '中国联通', type: 'bar', data: [-92, -98, -94, -98], itemStyle: { color: '#faad14' } }
    ]
  })

  chart2 = echarts.init(attenuationChart.value!)
  chart2.setOption({
    backgroundColor: 'transparent',
    xAxis: { name: '海拔' },
    yAxis: { name: 'RSRP' },
    series: [{
      symbolSize: 8,
      data: Array.from({length: 40}, (_, i) => [3600 + i * 50, -80 - i * 0.8 - Math.random() * 5]),
      type: 'scatter',
      itemStyle: { color: '#13c2c2' }
    }]
  })
}

const resize = () => {
  chart1?.resize()
  chart2?.resize()
}

onMounted(() => {
  initCharts()
})

defineExpose({ resize })
</script>

<style scoped>
.sidebar {
  width: 360px; height: 100%; padding: 20px; display: flex; flex-direction: column; gap: 20px; z-index: 10;
  overflow-y: auto; overflow-x: hidden;
  box-sizing: border-box;
}
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: rgba(24, 144, 255, 0.3); border-radius: 2px; }

.card {
  box-sizing: border-box;
  background: #ffffff; border: 1px solid #f0f0f0; border-radius: 12px;
  padding: 15px; min-height: 280px; flex-shrink: 0;
  display: flex; flex-direction: column;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.card-title { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid #f9f9f9; padding-bottom: 8px; }
.card h3 { font-size: 1.1rem; margin: 0; color: #001529; font-weight: bold; }
.chart-box { flex: 1; width: 100%; min-height: 180px; }

.stat-list { list-style: none; padding: 0; margin: 0; }
.stat-row { display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }
.stat-row .label { font-size: 0.9rem; color: #595959; }
.progress-bar { height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 4px; transition: width 1s ease-out; }
.green { color: #52c41a; } .yellow { color: #faad14; } .red { color: #ff4d4f; }
.progress-fill.green { background: #52c41a; }
.progress-fill.yellow { background: #faad14; }
.progress-fill.red { background: #ff4d4f; }

.bottom-spacer {
  height: 150px; /* 极端占位高度 */
  flex-shrink: 0;
}
</style>
