<template>
  <aside class="sidebar left-sidebar">
    <section class="card">
      <h3>运营商覆盖质量对比</h3>
      <div ref="rsrpChart" class="chart-box"></div>
    </section>

    <section class="card">
      <h3>海拔与信号衰减</h3>
      <div ref="attenuationChart" class="chart-box"></div>
    </section>

    <section class="card statistics-card">
      <h3>区域信号状态</h3>
      <ul class="stat-list">
        <li>
          <span>良好（>-90 dBm）</span>
          <div class="progress-bar"><div class="progress-fill green" style="width: 65%"></div></div>
          <strong class="green">65%</strong>
        </li>
        <li>
          <span>一般（-105~-90 dBm）</span>
          <div class="progress-bar"><div class="progress-fill yellow" style="width: 22%"></div></div>
          <strong class="yellow">22%</strong>
        </li>
        <li>
          <span>较弱（<-105 dBm）</span>
          <div class="progress-bar"><div class="progress-fill red" style="width: 13%"></div></div>
          <strong class="red">13%</strong>
        </li>
      </ul>
    </section>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
    legend: { top: 0, textStyle: { color: '#52606d' } },
    grid: { left: '3%', right: '4%', bottom: '6%', containLabel: true },
    xAxis: { type: 'category', data: ['拉萨', '日喀则', '昌都', '林芝'] },
    yAxis: { type: 'value', name: 'RSRP' },
    series: [
      { name: '中国移动', type: 'bar', data: [-85, -92, -88, -95], itemStyle: { color: '#2457a6' } },
      { name: '中国电信', type: 'bar', data: [-88, -95, -90, -92], itemStyle: { color: '#217a3d' } },
      { name: '中国联通', type: 'bar', data: [-92, -98, -94, -98], itemStyle: { color: '#b7791f' } }
    ]
  })

  chart2 = echarts.init(attenuationChart.value!)
  chart2.setOption({
    backgroundColor: 'transparent',
    tooltip: {},
    grid: { left: '3%', right: '4%', bottom: '6%', containLabel: true },
    xAxis: { name: '海拔', type: 'value' },
    yAxis: { name: 'RSRP', type: 'value' },
    series: [{
      symbolSize: 7,
      data: Array.from({ length: 40 }, (_, i) => [3600 + i * 50, -80 - i * 0.8 - Math.random() * 5]),
      type: 'scatter',
      itemStyle: { color: '#2457a6' }
    }]
  })
}

const resize = () => {
  chart1?.resize()
  chart2?.resize()
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
  border-right: 1px solid #d8dee6;
}

.card {
  min-height: 250px;
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
  flex: 1;
  width: 100%;
  min-height: 180px;
}

.stat-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.stat-list li {
  display: grid;
  grid-template-columns: 1fr 48px;
  gap: 8px;
  align-items: center;
  margin-bottom: 14px;
  color: #52606d;
  font-size: 13px;
}

.progress-bar {
  grid-column: 1 / -1;
  height: 8px;
  overflow: hidden;
  background: #e4e7eb;
  border-radius: 4px;
}

.progress-fill {
  height: 100%;
}

.green { color: #217a3d; }
.yellow { color: #b7791f; }
.red { color: #b42318; }

.progress-fill.green { background: #217a3d; }
.progress-fill.yellow { background: #d69e2e; }
.progress-fill.red { background: #b42318; }
</style>
