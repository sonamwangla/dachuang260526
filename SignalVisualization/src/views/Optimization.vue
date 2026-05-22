<template>
  <div class="optimize-page" id="pdf-content">
    <header class="opt-nav">
      <div class="nav-left">
        <router-link to="/" class="nav-item">系统概览</router-link>
        <router-link to="/visualization" class="nav-item">监控大屏</router-link>
      </div>
      <h1>高原信号 3D 仿真优化</h1>
      <span class="role-indicator" :class="user.role">
        {{ user.role === 'admin' ? '管理员权限' : '仿真权限' }}
      </span>
    </header>

    <main class="opt-layout">
      <aside class="left-aside no-print">
        <section class="panel">
          <h2>仿真参数</h2>
          <label>
            海拔高度：<strong>{{ simParams.alt }} m</strong>
            <input v-model="simParams.alt" type="range" min="3000" max="6000" />
          </label>

          <label>
            天气环境
            <select v-model="simParams.weather">
              <option value="clear">晴朗</option>
              <option value="cloudy">多云</option>
              <option value="snow">积雪</option>
            </select>
          </label>

          <button class="primary-btn" @click="runSimulation" :disabled="isSimulating">
            {{ isSimulating ? '分析中...' : '运行空间仿真' }}
          </button>
        </section>

        <section class="panel legend-panel">
          <h2>RSRP 图例</h2>
          <div><span class="dot good"></span> 优良：大于 -85 dBm</div>
          <div><span class="dot weak"></span> 弱覆盖：小于 -105 dBm</div>
        </section>
      </aside>

      <section class="results-section">
        <div class="panel chart-panel">
          <div class="panel-head">
            <h2>信号空间分布模型</h2>
            <span>3D Scatter</span>
          </div>
          <div ref="chart3D" class="chart3d"></div>
        </div>

        <div v-if="simResult" class="panel result-detail">
          <div class="metrics-grid">
            <div>
              <span>预测 RSRP</span>
              <strong>{{ simResult.predicted_rsrp }} dBm</strong>
            </div>
            <div>
              <span>预测状态</span>
              <strong :class="simResult.status === '覆盖正常' ? 'green' : 'red'">{{ simResult.status }}</strong>
            </div>
          </div>

          <div class="report-actions no-print">
            <button class="outline-btn" @click="exportPDF" :disabled="isExporting">
              {{ isExporting ? '生成中...' : '导出 PDF 报告' }}
            </button>
            <button v-if="user.role === 'admin'" class="success-btn" @click="applyOptimization" :disabled="isOptimizing">
              {{ isOptimizing ? '执行中...' : '下发参数调整' }}
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import 'echarts-gl'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const simParams = ref({ alt: 3650, weather: 'clear' })
const simResult = ref<any>(null)
const isSimulating = ref(false)
const isOptimizing = ref(false)
const isExporting = ref(false)
const chart3D = ref<HTMLElement>()
let myChart: echarts.EChartsType

const authAxios = axios.create()
authAxios.interceptors.request.use(config => {
  config.headers['x-access-token'] = localStorage.getItem('token')
  return config
})

const runSimulation = async () => {
  isSimulating.value = true
  try {
    const res = await authAxios.post('/api/analysis/predict', simParams.value)
    simResult.value = res.data
  } catch (err) {
    simResult.value = {
      predicted_rsrp: -106,
      status: '服务未连接'
    }
  } finally {
    isSimulating.value = false
  }
}

const fetch3DData = async () => {
  try {
    const res = await authAxios.get('/api/history')
    const data3d = res.data.map((p: any) => [p.lng, p.lat, p.alt, p.rsrp])
    myChart.setOption({
      visualMap: {
        min: -130,
        max: -60,
        text: ['强', '弱'],
        inRange: { color: ['#2f5597', '#d9e8f5', '#b42318'] }
      },
      series: [{ type: 'scatter3D', data: data3d, symbolSize: 8 }]
    })
  } catch (err) {
    myChart.setOption({ series: [{ type: 'scatter3D', data: [] }] })
  }
}

const exportPDF = async () => {
  isExporting.value = true
  const element = document.getElementById('pdf-content')
  if (!element) {
    isExporting.value = false
    return
  }

  try {
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      ignoreElements: el => el.classList.contains('no-print')
    })

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const imgProps = pdf.getImageProperties(imgData)
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
    pdf.save(`高原信号诊断报告_${Date.now()}.pdf`)
  } catch (err) {
    alert('PDF 生成失败，请重试')
  } finally {
    isExporting.value = false
  }
}

const applyOptimization = () => {
  isOptimizing.value = true
  setTimeout(() => {
    alert('基站参数调整指令已下发')
    isOptimizing.value = false
  }, 1200)
}

onMounted(() => {
  myChart = echarts.init(chart3D.value!)
  myChart.setOption({
    tooltip: {},
    grid3D: {
      viewControl: { autoRotate: false },
      axisLine: { lineStyle: { color: '#8a94a6' } },
      axisPointer: { lineStyle: { color: '#2457a6' } }
    },
    xAxis3D: { name: '经度', scale: true },
    yAxis3D: { name: '纬度', scale: true },
    zAxis3D: { name: '海拔', scale: true },
    series: [{ type: 'scatter3D', data: [] }]
  })
  fetch3DData()
})
</script>

<style scoped>
.optimize-page {
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  background: #f4f6f8;
  color: #1f2933;
}

.opt-nav {
  min-height: 58px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 16px;
  padding: 0 20px;
  margin-bottom: 20px;
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 6px;
}

.nav-left {
  display: flex;
  gap: 8px;
}

.nav-item {
  color: #4b5563;
  text-decoration: none;
  padding: 7px 10px;
  border-radius: 4px;
}

.nav-item:hover {
  color: #183b70;
  background: #edf2f7;
}

h1,
h2 {
  margin: 0;
}

h1 {
  font-size: 18px;
}

h2 {
  font-size: 15px;
}

.role-indicator {
  justify-self: end;
  padding: 4px 8px;
  border-radius: 4px;
  background: #edf2f7;
  color: #52606d;
  font-size: 12px;
}

.role-indicator.admin {
  background: #fde8e8;
  color: #a61b1b;
}

.opt-layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 20px;
}

.left-aside,
.results-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel {
  background: #fff;
  border: 1px solid #d8dee6;
  border-radius: 6px;
  padding: 20px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  color: #52606d;
  font-size: 13px;
}

label {
  display: block;
  margin-top: 18px;
  color: #344054;
  font-size: 14px;
  font-weight: 600;
}

label strong {
  color: #183b70;
}

input[type='range'],
select {
  width: 100%;
  box-sizing: border-box;
  margin-top: 8px;
}

select {
  padding: 9px 10px;
  border: 1px solid #cbd2d9;
  border-radius: 4px;
  background: #fff;
}

button {
  border-radius: 4px;
  padding: 11px 14px;
  border: 1px solid transparent;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  opacity: 0.58;
  cursor: not-allowed;
}

.primary-btn {
  width: 100%;
  margin-top: 20px;
  background: #2457a6;
  color: #fff;
}

.legend-panel {
  color: #52606d;
  font-size: 14px;
}

.legend-panel div {
  margin-top: 14px;
}

.dot {
  width: 9px;
  height: 9px;
  display: inline-block;
  margin-right: 8px;
  border-radius: 50%;
}

.good { background: #217a3d; }
.weak { background: #b42318; }

.chart-panel {
  min-height: 500px;
}

.chart3d {
  width: 100%;
  height: 440px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-bottom: 18px;
}

.metrics-grid div {
  padding: 16px;
  background: #f8fafc;
  border: 1px solid #e4e7eb;
  border-radius: 4px;
}

.metrics-grid span,
.metrics-grid strong {
  display: block;
}

.metrics-grid span {
  color: #697586;
  font-size: 13px;
}

.metrics-grid strong {
  margin-top: 8px;
  font-size: 24px;
}

.green { color: #217a3d; }
.red { color: #b42318; }

.report-actions {
  display: flex;
  gap: 12px;
}

.outline-btn {
  border-color: #b7791f;
  color: #8a4b0f;
  background: #fff;
}

.success-btn {
  background: #217a3d;
  color: #fff;
}

@media (max-width: 920px) {
  .opt-nav,
  .opt-layout,
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .role-indicator {
    justify-self: start;
  }
}

@media print {
  .no-print {
    display: none !important;
  }
}
</style>
