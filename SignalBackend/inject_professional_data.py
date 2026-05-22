import numpy as np
import pandas as pd
from app import app, db, SignalRecord
import datetime
import random

# --- 物理参数配置 ---
FREQ_MHZ = 1800  # 载波频率
BASE_POWER = 43  # 基站发射功率 (dBm)
ANTENNA_GAIN = 15 # 天线增益 (dBi)
SAMPLE_COUNT = 5000 # 生成 5000 条数据

# 预设基站坐标 (拉萨核心区及周边)
BASE_STATIONS = [
    {"name": "布达拉宫基站", "lat": 29.657, "lng": 91.117, "carrier": "中国移动", "alt": 3700},
    {"name": "大昭寺基站", "lat": 29.653, "lng": 91.131, "carrier": "中国电信", "alt": 3650},
    {"name": "拉萨火车站基站", "lat": 29.628, "lng": 91.065, "carrier": "中国联通", "alt": 3640},
    {"name": "色拉寺北侧基站", "lat": 29.701, "lng": 91.132, "carrier": "中国移动", "alt": 3850},
    {"name": "纳金路东段基站", "lat": 29.665, "lng": 91.185, "carrier": "中国电信", "alt": 3660}
]

def calculate_rsrp(dist_km, alt, carrier):
    """
    基于物理模型的 RSRP 计算函数
    """
    fspl = 32.44 + 20 * np.log10(FREQ_MHZ) + 20 * np.log10(max(dist_km, 0.01))
    alt_penalty = max(0, (alt - 3600) / 100) * 0.8
    shadowing = np.random.normal(0, 4.5)
    rsrp = BASE_POWER + ANTENNA_GAIN - fspl - alt_penalty - shadowing
    
    # 运营商差异修正
    if "移动" in carrier: rsrp += 2
    elif "联通" in carrier: rsrp -= 3
    
    return int(np.clip(rsrp, -140, -50))

def run_injection():
    with app.app_context():
        print("--- 正在清理旧数据 ---")
        db.session.query(SignalRecord).delete()
        
        print(f"--- 正在生成 {SAMPLE_COUNT} 条高原专业模拟数据 (混合运营商) ---")
        
        records = []
        for i in range(SAMPLE_COUNT):
            lat = 29.62 + np.random.rand() * 0.08
            lng = 91.05 + np.random.rand() * 0.15
            alt = 3630 + (lat - 29.62) * 2000 + np.random.rand() * 50
            
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
                device_id=f"Tibet-Probe-{random.randint(100, 999)}",
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0, 1440))
            )
            records.append(record)
            
            if i % 1000 == 0 and i > 0:
                print(f"已生成 {i} 条...")

        db.session.bulk_save_objects(records)
        db.session.commit()
        print(f"--- 成功注入 {SAMPLE_COUNT} 条混合数据，数据库已就绪！ ---")

if __name__ == "__main__":
    run_injection()
