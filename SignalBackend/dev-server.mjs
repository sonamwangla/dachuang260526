import http from 'node:http'

const PORT = 5000
const SECRET_TOKEN = 'dev-token'

const users = {
  admin: { password: 'sonam101', role: 'admin' },
  operator_01: { password: 'password123', role: 'operator' },
  viewer_guest: { password: 'guest_password', role: 'viewer' }
}

const carriers = ['中国移动', '中国电信', '中国联通']

const history = Array.from({ length: 220 }, (_, index) => {
  const timestamp = new Date(Date.now() - index * 38_000)
  const rsrp = -82 - Math.round(Math.random() * 40)

  return {
    id: index + 1,
    lat: Number((29.655 + (Math.random() - 0.5) * 0.052).toFixed(6)),
    lng: Number((91.125 + (Math.random() - 0.5) * 0.084).toFixed(6)),
    alt: Number((3600 + Math.random() * 520).toFixed(1)),
    rsrp,
    sinr: Number((8 + Math.random() * 18).toFixed(1)),
    carrier: carriers[index % carriers.length],
    device_id: `Device-${String(24 + (index % 16)).padStart(3, '0')}`,
    time: timestamp.toLocaleTimeString('zh-CN', { hour12: false })
  }
})

const sendJson = (res, status, data) => {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, x-access-token',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
  })
  res.end(JSON.stringify(data))
}

const readBody = req => new Promise(resolve => {
  let body = ''
  req.on('data', chunk => {
    body += chunk
  })
  req.on('end', () => {
    try {
      resolve(body ? JSON.parse(body) : {})
    } catch {
      resolve({})
    }
  })
})

const requireToken = (req, res) => {
  const token = req.headers['x-access-token']
  if (!token) {
    sendJson(res, 401, { msg: 'Token is missing' })
    return false
  }
  return true
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    sendJson(res, 200, {})
    return
  }

  if (req.url === '/api/auth/login' && req.method === 'POST') {
    const body = await readBody(req)
    const user = users[body.username]

    if (!user || user.password !== body.password) {
      sendJson(res, 401, { msg: '账号或密码错误' })
      return
    }

    sendJson(res, 200, {
      token: SECRET_TOKEN,
      user: { username: body.username, role: user.role }
    })
    return
  }

  if (req.url === '/api/auth/register' && req.method === 'POST') {
    const body = await readBody(req)
    if (!body.username || !body.password) {
      sendJson(res, 400, { msg: '用户名和密码不能为空' })
      return
    }

    users[body.username] = {
      password: body.password,
      role: body.role || 'operator'
    }
    sendJson(res, 201, { msg: 'Success' })
    return
  }

  if (req.url === '/api/history' && req.method === 'GET') {
    if (!requireToken(req, res)) return
    sendJson(res, 200, history)
    return
  }

  if (req.url === '/api/analysis/predict' && req.method === 'POST') {
    if (!requireToken(req, res)) return
    const body = await readBody(req)
    const alt = Number(body.alt || 3650)
    const predicted = -88 - Math.round((alt - 3600) / 120) - Math.round(Math.random() * 8)

    sendJson(res, 200, {
      predicted_rsrp: predicted,
      status: predicted > -95 ? '覆盖正常' : predicted > -105 ? '边缘覆盖' : '弱覆盖',
      suggestion: predicted > -105 ? '建议持续观察邻区切换质量。' : '建议补充微基站并校正天线方位角。',
      suggestions: [
        '核查最近基站负载和邻区切换门限。',
        '结合地形遮挡情况调整天线下倾角。',
        '对弱覆盖路段补充定点采样。'
      ],
      environment: { status: alt > 4500 ? '极高海拔环境' : '常规高原环境' }
    })
    return
  }

  if (req.url === '/api/upload' && req.method === 'POST') {
    if (!requireToken(req, res)) return
    const body = await readBody(req)
    const record = {
      id: history.length + 1,
      lat: body.lat,
      lng: body.lng,
      alt: body.alt || 3650,
      rsrp: body.rsrp,
      sinr: body.sinr || 15,
      carrier: body.carrier || '中国移动',
      device_id: body.device_id || 'Device-01',
      time: new Date().toLocaleTimeString('zh-CN', { hour12: false })
    }
    history.unshift(record)
    sendJson(res, 200, { status: 'success', id: record.id })
    return
  }

  sendJson(res, 404, { msg: 'Not found' })
})

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Dev backend listening on http://127.0.0.1:${PORT}`)
})
