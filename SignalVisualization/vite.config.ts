import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

const users: Record<string, { password: string; role: string }> = {
  admin: { password: 'sonam101', role: 'admin' },
  operator_01: { password: 'password123', role: 'operator' },
  viewer_guest: { password: 'guest_password', role: 'viewer' },
}

const carriers = ['China Mobile', 'China Telecom', 'China Unicom']
const history = Array.from({ length: 220 }, (_, index) => {
  const timestamp = new Date(Date.now() - index * 38000)
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
    time: timestamp.toLocaleTimeString('zh-CN', { hour12: false }),
  }
})

function readJson(req: any) {
  return new Promise<any>((resolve) => {
    let body = ''
    req.on('data', (chunk: Buffer) => {
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
}

function sendJson(res: any, status: number, data: unknown) {
  res.statusCode = status
  res.setHeader('Content-Type', 'application/json; charset=utf-8')
  res.end(JSON.stringify(data))
}

function devApiPlugin() {
  return {
    name: 'local-dev-api',
    configureServer(server: any) {
      server.middlewares.use('/api', async (req: any, res: any) => {
        const url = req.url?.split('?')[0] || '/'
        const method = req.method || 'GET'

        if (url === '/auth/login' && method === 'POST') {
          const body = await readJson(req)
          const user = users[body.username]
          if (!user || user.password !== body.password) {
            sendJson(res, 401, { msg: 'Login failed' })
            return
          }
          sendJson(res, 200, { token: 'dev-token', user: { username: body.username, role: user.role } })
          return
        }

        if (url === '/auth/register' && method === 'POST') {
          const body = await readJson(req)
          if (!body.username || !body.password) {
            sendJson(res, 400, { msg: 'Username and password are required' })
            return
          }
          users[body.username] = { password: body.password, role: body.role || 'operator' }
          sendJson(res, 201, { msg: 'Success' })
          return
        }

        if (url === '/history' && method === 'GET') {
          sendJson(res, 200, history)
          return
        }

        if (url === '/upload' && method === 'POST') {
          const body = await readJson(req)
          const record = {
            id: history.length + 1,
            lat: body.lat,
            lng: body.lng,
            alt: body.alt || 3650,
            rsrp: body.rsrp,
            sinr: body.sinr || 15,
            carrier: body.carrier || 'China Mobile',
            device_id: body.device_id || 'Device-01',
            time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
          }
          history.unshift(record)
          sendJson(res, 200, { status: 'success', id: record.id })
          return
        }

        if (url === '/analysis/predict' && method === 'POST') {
          const body = await readJson(req)
          const alt = Number(body.alt || 3650)
          const predicted = -88 - Math.round((alt - 3600) / 120) - Math.round(Math.random() * 8)
          sendJson(res, 200, {
            predicted_rsrp: predicted,
            status: predicted > -95 ? 'Normal coverage' : predicted > -105 ? 'Edge coverage' : 'Weak coverage',
            suggestions: [
              'Check nearby base-station load and handover thresholds.',
              'Adjust antenna tilt based on terrain obstruction.',
              'Add fixed-point samples on weak coverage road sections.',
            ],
            environment: { status: alt > 4500 ? 'High-altitude environment' : 'Plateau environment' },
          })
          return
        }

        sendJson(res, 404, { msg: 'Not found' })
      })
    },
  }
}

export default defineConfig({
  plugins: [vue(), devApiPlugin()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
