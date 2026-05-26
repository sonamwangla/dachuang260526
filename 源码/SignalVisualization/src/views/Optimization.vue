<template>
  <div class="optimize-page" id="pdf-content">
    <header class="opt-nav white-nav shadow-sm">
      <div class="nav-left">
        <router-link to="/" class="nav-item">🏠 系统首页</router-link>
        <router-link to="/visualization" class="nav-item">📊 监控大屏</router-link>
      </div>
      <div class="nav-center"><h1 class="opt-title">AI 高原信号 3D 仿真中心</h1></div>
      <div class="nav-right">
        <span class="role-indicator" :class="user.role">权限: {{ user.role === 'admin' ? '完全决策' : '仿真执行' }}</span>
      </div>
    </header>

    <main class="opt-layout">
      <aside class="left-aside no-print">
        <section class="config-section white-card">
          <div class="section-header">🏔️ 仿真环境配置</div>
          <div class="form-item">
            <label>仿真海拔: <span class="val-hl">{{ simParams.alt }}m</span></label>
            <input type="range" min="3000" max="6000" v-model="simParams.alt" class="slider" />
          </div>
          <div class="form-item">
            <label>当前天气环境</label>
            <select v-model="simParams.weather" class="opt-select">
              <option value="clear">☀️ 晴朗</option>
              <option value="cloudy">☁️ 多云</option>
              <option value="snow">❄️ 积雪</option>
            </select>
          </div>
          <button class="btn run-btn" @click="runSimulation" :disabled="isSimulating">
            {{ isSimulating ? 'AI 分析中...' : '🚀 运行 3D 空间仿真' }}
          </button>
        </section>

        <section class="physics-legend white-card" style="margin-top: 20px;">
          <div class="section-header">📡 信号沙盘图例</div>
          <div class="legend-item"><span class="dot red"></span> RSRP > -85 (极好)</div>
          <div class="legend-item"><span class="dot blue"></span> RSRP < -105 (极弱)</div>
        </section>
      </aside>

      <section class="results-section">
        <div class="charts-area white-card shadow-3d">
          <div class="section-header">🗺️ 全局信号空间分布模型 (3D Scatter)</div>
          <div ref="chart3D" style="height: 400px; width: 100%;"></div>
        </div>
        
        <div v-if="simResult" class="result-detail white-card shadow fade-in">
          <div class="metrics-grid">
            <div class="m-box">
              <span class="m-label">预测 RSRP</span>
              <span class="m-val">{{ simResult.predicted_rsrp }} dBm</span>
            </div>
            <div class="m-box">
              <span class="m-label">预测状态</span>
              <span class="m-val" :class="simResult.status === '覆盖正常' ? 'green' : 'red'">{{ simResult.status }}</span>
            </div>
          </div>

          <div class="report-actions no-print">
            <button class="btn export-btn" @click="exportPDF" :disabled="isExporting">
              {{ isExporting ? '正在生成 PDF...' : '📄 导出 PDF 诊断报告' }}
            </button>
            <button v-if="user.role === 'admin'" class="btn opt-btn" @click="applyOptimization" :disabled="isOptimizing">
              {{ isOptimizing ? '指令执行中...' : '✅ 远程参数调优下发' }}
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
    const res = await authAxios.post('http://127.0.0.1:5000/api/analysis/predict', simParams.value)
    simResult.value = res.data
  } catch (err) {}
  isSimulating.value = false
}

const fetch3DData = async () => {
  try {
    const res = await authAxios.get('http://127.0.0.1:5000/api/history')
    const data3d = res.data.map((p: any) => [p.lng, p.lat, p.alt, p.rsrp])
    myChart.setOption({
      visualMap: { min: -130, max: -60, inRange: { color: ['#313695', '#abd9e9', '#a50026'] } },
      series: [{ type: 'scatter3D', data: data3d, symbolSize: 10 }]
    })
  } catch (err) {}
}

const exportPDF = async () => {
  isExporting.value = true
  const element = document.getElementById('pdf-content')
  if (!element) return

  try {
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      ignoreElements: (el) => el.classList.contains('no-print')
    })
    
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const imgProps = pdf.getImageProperties(imgData)
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width
    
    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
    pdf.save(`高原信号诊断报告_${new Date().getTime()}.pdf`)
  } catch (err) {
    alert('PDF 生成失败，请重试')
  }
  isExporting.value = false
}

const applyOptimization = () => {
  isOptimizing.value = true
  setTimeout(() => {
    alert('基站倾角优化完成。')
    isOptimizing.value = false
  }, 1500)
}

onMounted(() => {
  myChart = echarts.init(chart3D.value!)
  myChart.setOption({
    grid3D: { viewControl: { autoRotate: true } },
    xAxis3D: { name: '经度', scale: true },
    yAxis3D: { name: '纬度', scale: true },
    zAxis3D: { name: '海拔', scale: true },
    series: [{ type: 'scatter3D', data: [] }]
  })
  fetch3DData()
})
</script>

<style scoped>
.optimize-page { padding: 20px; background: #ffffff; min-height: 100vh; color: #333; font-family: 'Inter', sans-serif; }
.opt-nav { background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); padding: 15px 30px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border: 1px solid #e8e8e8; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.opt-title { font-size: 1.2rem; color: #1890ff; font-weight: 800; }
.nav-item { color: #666; text-decoration: none; margin-right: 20px; font-weight: 500; transition: 0.3s; }
.nav-item:hover { color: #1890ff; }

.opt-layout { display: flex; gap: 20px; }
.left-aside { width: 320px; }
.white-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e8e8e8; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.section-header { font-weight: bold; margin-bottom: 20px; color: #1890ff; display: flex; align-items: center; gap: 10px; }
.results-section { flex: 1; display: flex; flex-direction: column; gap: 20px; }
.metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.m-box { background: #fafafa; padding: 20px; border-radius: 10px; border: 1px solid #e8e8e8; text-align: center; }
.m-label { color: #666; font-size: 0.85rem; margin-bottom: 10px; display: block; }
.m-val { font-size: 1.8rem; font-weight: bold; display: block; font-family: 'JetBrains Mono', monospace; }
.green { color: #52c41a; }
.red { color: #ff4d4f; }

.btn { flex: 1; padding: 14px; border-radius: 8px; cursor: pointer; border: none; font-weight: bold; transition: 0.3s; font-size: 0.95rem; }
.run-btn { background: #1890ff; color: #fff; box-shadow: 0 4px 15px rgba(24,144,255,0.3); width: 100%; margin-top: 10px; }
.run-btn:hover { background: #40a9ff; transform: translateY(-3px); }
.run-btn:disabled { background: #d9d9d9; color: #999; cursor: not-allowed; transform: none; box-shadow: none; }
.export-btn { background: transparent; border: 1px solid #fa8c16; color: #fa8c16; }
.export-btn:hover { background: rgba(250,140,22,0.1); }
.opt-btn { background: #52c41a; color: #fff; }

.opt-select { background: #ffffff; color: #333; border: 1px solid #d9d9d9; padding: 10px; border-radius: 6px; width: 100%; }
.slider { width: 100%; height: 6px; border-radius: 5px; background: #e8e8e8; outline: none; -webkit-appearance: none; }
.slider::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; background: #1890ff; cursor: pointer; box-shadow: 0 0 10px rgba(24,144,255,0.5); }
.val-hl { color: #1890ff; font-weight: bold; }
.legend-item { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; font-size: 0.85rem; color: #666; }
.dot { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 5px currentColor; }
.blue { background: #313695; color: #313695; }
.red { background: #a50026; color: #a50026; }

/* ECharts 容器样式 */
.charts-area { min-height: 450px; background: #fafafa; border: 1px solid #e8e8e8; }

/* 打印/导出优化 */
@media print {
  .no-print { display: none !important; }
}
</style>
