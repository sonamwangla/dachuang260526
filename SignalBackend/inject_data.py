import sqlite3
import datetime
import random
import os

db_path = os.path.join(os.path.dirname(__file__), 'signals.db')

def inject_mock_data():
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 清空现有数据
    try:
        cursor.execute("DELETE FROM signal_record")
    except sqlite3.OperationalError:
        print("表 signal_record 不存在，请确保后端已运行并初始化了数据库。")
        conn.close()
        return
    
    # 插入 100 条模拟记录
    base_lat, base_lng = 29.655, 91.125
    carriers = ['中国移动', '中国电信', '中国联通']
    
    records = []
    for _ in range(100):
        lat = base_lat + (random.random() - 0.5) * 0.05
        lng = base_lng + (random.random() - 0.5) * 0.08
        alt = 3600 + random.random() * 500
        rsrp = int(-80 - random.random() * 45)
        sinr = round(random.random() * 25, 1)
        carrier = random.choice(carriers)
        device_id = f"Device-{random.randint(10, 99)}"
        timestamp = (datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0, 1440))).strftime('%Y-%m-%d %H:%M:%S')
        
        records.append((lat, lng, alt, rsrp, sinr, carrier, device_id, timestamp))
    
    cursor.executemany("""
        INSERT INTO signal_record (lat, lng, alt, rsrp, sinr, carrier, device_id, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()
    print("成功向数据库注入 100 条模拟数据。")

if __name__ == "__main__":
    inject_mock_data()
