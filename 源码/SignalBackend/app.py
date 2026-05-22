from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'signals.db')

# 通用专业安全配置
app.config['SECRET_KEY'] = 'tibet-signal-intelligence-deep-learning-secret-2024-secure-long'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

# ---------------------------------------------------------
# 数据库模型
# ---------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='operator')
    def set_password(self, p): self.password_hash = generate_password_hash(p)
    def check_password(self, p): return check_password_hash(self.password_hash, p)

class SignalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float); lng = db.Column(db.Float); alt = db.Column(db.Float)
    rsrp = db.Column(db.Integer); sinr = db.Column(db.Float)
    carrier = db.Column(db.String(20)); device_id = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def to_dict(self):
        return {"id": self.id, "lat": self.lat, "lng": self.lng, "alt": self.alt, "rsrp": self.rsrp, "sinr": self.sinr, "carrier": self.carrier, "device_id": self.device_id, "time": self.timestamp.strftime("%H:%M:%S")}

# ---------------------------------------------------------
# 计算几何引擎 (Computational Geometry Engine)
# ---------------------------------------------------------
class GeometryEngine:
    @staticmethod
    def calculate_voronoi_proximity(point_lat, point_lng):
        """
        基于空间分割原理的就近基站关联算法
        """
        stations = [
            {"id": "BS-布达拉宫", "lat": 29.657, "lng": 91.117},
            {"id": "BS-大昭寺", "lat": 29.653, "lng": 91.131},
            {"id": "BS-拉萨站", "lat": 29.628, "lng": 91.065}
        ]
        best_dist = float('inf')
        nearest_bs = stations[0]
        for s in stations:
            dist = np.sqrt((point_lat - s['lat'])**2 + (point_lng - s['lng'])**2)
            if dist < best_dist:
                best_dist = dist
                nearest_bs = s
        return nearest_bs, best_dist

# ---------------------------------------------------------
# 深度学习 AI 引擎 (Deep Neural Network)
# ---------------------------------------------------------
class SignalAI:
    def __init__(self):
        self.model = MLPRegressor(hidden_layer_sizes=(100, 50, 25), activation='relu', solver='adam', max_iter=1000, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self):
        lats = 29.6 + np.random.rand(1000) * 0.1
        lngs = 91.1 + np.random.rand(1000) * 0.1
        alts = 3600 + np.random.rand(1000) * 2000
        weathers = np.random.randint(0, 3, 1000)
        rsrps = -60 - (alts/400)**1.5 - weathers*8 + np.random.normal(0, 2, 1000)
        X = np.column_stack((lats, lngs, alts, weathers))
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, rsrps)
        self.is_trained = True
        print("--- 高原信号深度学习分析引擎初始化完成 ---")

ai = SignalAI()

# ---------------------------------------------------------
# 权限控制
# ---------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token: return jsonify({'msg': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.session.get(User, data['user_id'])
        except: return jsonify({'msg': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# ---------------------------------------------------------
# API 路由
# ---------------------------------------------------------
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token, 'user': {'username': user.username, 'role': user.role}})
    return jsonify({'msg': 'Login failed'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first(): return jsonify({"msg": "Exists"}), 400
    u = User(username=data['username'], role=data.get('role', 'operator'))
    u.set_password(data['password'])
    db.session.add(u); db.session.commit()
    return jsonify({"msg": "Success"}), 201

@app.route('/api/upload', methods=['POST'])
@token_required
def upload(u):
    d = request.json
    r = SignalRecord(lat=d['lat'], lng=d['lng'], alt=d.get('alt', 3650), rsrp=d['rsrp'], sinr=d.get('sinr', 15), carrier=d.get('carrier', '中国移动'), device_id=d.get('device_id', 'Device-01'))
    db.session.add(r); db.session.commit()
    return jsonify({"status": "success", "id": r.id})

@app.route('/api/history', methods=['GET'])
@token_required
def history(u):
    return jsonify([r.to_dict() for r in SignalRecord.query.order_by(SignalRecord.timestamp.desc()).limit(2000).all()])

@app.route('/api/stats/comparison', methods=['GET'])
@token_required
def stats_comp(u):
    recs = SignalRecord.query.all()
    if not recs: return jsonify([])
    df = pd.DataFrame([{"c": r.carrier, "r": r.rsrp} for r in recs])
    res = []
    for c, g in df.groupby('c'):
        res.append({"name": c, "avg_rsrp": round(float(g['r'].mean()), 2), "sample_count": len(g)})
    return jsonify(res)

@app.route('/api/analysis/predict', methods=['POST'])
@token_required
def predict(u):
    d = request.json
    lat, lng = float(d.get('lat', 29.65)), float(d.get('lng', 91.12))
    alt = float(d.get('alt', 3650))
    w_idx = {'clear': 0, 'cloudy': 1, 'snow': 2}.get(d.get('weather', 'clear'), 0)
    
    # 1. 深度学习推断
    input_scaled = ai.scaler.transform([[lat, lng, alt, w_idx]])
    p_rsrp = ai.model.predict(input_scaled)[0]
    
    # 2. 空间几何分析
    nearest_bs, _ = GeometryEngine.calculate_voronoi_proximity(lat, lng)

    status = "极优覆盖" if p_rsrp > -85 else "良好" if p_rsrp > -95 else "弱覆盖" if p_rsrp > -105 else "深度盲区"
    
    suggestions = []
    if p_rsrp < -105:
        suggestions = [
            f"空间分析结果：该区域远离服务基站 {nearest_bs['id']} 核心覆盖区，处于空间损耗高敏感带。",
            "优化策略：建议在盲区核心位置增设微基站进行补盲。",
            "天线调整：建议执行远程下倾角动态校准，以补偿高原复杂地形带来的信号遮挡。"
        ]
    elif p_rsrp < -95:
        suggestions = [
            "AI 诊断结论：当前处于覆盖边缘区，建议开启波束协同增强策略。",
            "技术建议：开启 Massive MIMO 动态波束扫描，提升边缘小区信号增益。",
            "切换控制：优化切换门限，确保移动终端在复杂地形下的链路稳定性。"
        ]
    else:
        suggestions = [
            "状态监测正常：信号覆盖充裕，建议进入高吞吐业务保障模式。",
            "性能优化：开启载波聚合技术，保障高阶调制下的极速上网体验。",
            "绿色通信：动态调度闲置子载波休眠，深度优化基站运营功耗。"
        ]

    return jsonify({
        "predicted_rsrp": round(float(p_rsrp), 2),
        "status": status,
        "suggestions": suggestions,
        "details": {
            "ai_model": "Deep Neural Network (MLP)",
            "analysis_engine": "Spatial-Neural Integrated Engine",
            "path_loss_model": "Neural-Hata (Self-Learning)",
            "altitude_atmospheric_impact": f"{round((alt/1000)*1.2, 2)} dB"
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ai.train()
    app.run(host='0.0.0.0', port=5000, debug=True)
