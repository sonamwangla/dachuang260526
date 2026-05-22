import numpy as np
import time
import random
import datetime
from app import app, db, SignalRecord

# --- 物理参数配置 ---
FREQ_MHZ = 1800  # 载波频率
BASE_POWER = 43  # 基站发射功率 (dBm)
ANTENNA_GAIN = 15 # 天线增益 (dBi)

# 预设基站坐标 (拉萨核心区及周边)
BASE_STATIONS = [
    {"name": "布达拉宫基站", "lat": 29.657, "lng": 91.117, "carrier": "中国移动", "alt": 3700},
    {"name": "大昭寺基站", "lat": 29.653, "lng": 91.131, "carrier": "中国电信", "alt": 3650},
    {"name": "拉萨火车站基站", "lat": 29.628, "lng": 91.065, "carrier": "中国联通", "alt": 3640},
    {"name": "色拉寺北侧基站", "lat": 29.701, "lng": 91.132, "carrier": "中国移动", "alt": 3850},
    {"name": "纳金路东段基站", "lat": 29.665, "lng": 91.185, "carrier": "中国电信", "alt": 3660}
]

def calculate_rsrp(dist_km, alt, carrier):
    # 1. 自由空间损耗 (FSPL)
    fspl = 32.44 + 20 * np.log10(FREQ_MHZ) + 20 * np.log10(max(dist_km, 0.01))
    # 2. 高原修正 (海拔衰减)
    alt_penalty = max(0, (alt - 3600) / 100) * 0.8
    # 3. 阴影衰减 (高斯噪声)
    shadowing = np.random.normal(0, 4.5)
    # 计算最终 RSRP
    rsrp = BASE_POWER + ANTENNA_GAIN - fspl - alt_penalty - shadowing
    # 运营商差异修正
    if "移动" in carrier: rsrp += 2
    elif "联通" in carrier: rsrp -= 3
    return int(np.clip(rsrp, -140, -50))

def run_simulator():
    print("--- 实时信号模拟器启动 ---")
    print("按 Ctrl+C 停止模拟...")
    
    with app.app_context():
        try:
            while True:
                # 在拉萨市区随机撒点模拟移动采集
                lat = 29.62 + np.random.rand() * 0.08
                lng = 91.05 + np.random.rand() * 0.15
                alt = 3630 + (lat - 29.62) * 2000 + np.random.rand() * 50
                
                # 寻找最近基站并计算信号
                best_rsrp = -140
                selected_carrier = "中国移动"
                for bs in BASE_STATIONS:
                    dist = np.sqrt((lat - bs['lat'])**2 + (lng - bs['lng'])**2) * 111
                    current_rsrp = calculate_rsrp(dist, alt, bs['carrier'])
                    if current_rsrp > best_rsrp:
                        best_rsrp = current_rsrp
                        selected_carrier = bs['carrier']
                
                record = SignalRecord(
                    lat=round(float(lat), 6),
                    lng=round(float(lng), 6),
                    alt=round(float(alt), 1),
                    rsrp=best_rsrp,
                    sinr=round(float(np.random.normal(12, 5)), 1),
                    carrier=selected_carrier,
                    device_id=f"Sim-Probe-{random.randint(100, 999)}",
                    timestamp=datetime.datetime.utcnow()
                )
                
                db.session.add(record)
                db.session.commit()
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 生成模拟数据: {selected_carrier} | RSRP: {best_rsrp} dBm | 位置: ({lat:.4f}, {lng:.4f})")
                
                # 随机等待 2-5 秒生成下一条
                time.sleep(random.uniform(2, 5))
                
        except KeyboardInterrupt:
            print("\n--- 模拟器已停止 ---")

if __name__ == "__main__":
    run_simulator()
