import axios, { type AxiosRequestConfig, type AxiosResponse } from 'axios'

type User = { password: string; role: string }
type SignalPoint = {
  id: number
  lat: number
  lng: number
  alt: number
  rsrp: number
  sinr: number
  carrier: string
  device_id: string
  time: string
}

const enabled = import.meta.env.VITE_STATIC_DEMO === '1'

const users: Record<string, User> = {
  admin: { password: 'sonam101', role: 'admin' },
  operator_01: { password: 'password123', role: 'operator' },
  viewer_guest: { password: 'guest_password', role: 'viewer' },
}

const carriers = ['China Mobile', 'China Telecom', 'China Unicom']
const history: SignalPoint[] = Array.from({ length: 220 }, (_, index) => {
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
    time: timestamp.toLocaleTimeString('zh-CN', { hour12: false }),
  }
})

function readBody(data: unknown) {
  if (!data) return {}
  if (typeof data === 'string') {
    try {
      return JSON.parse(data)
    } catch {
      return {}
    }
  }
  return data as Record<string, any>
}

function response(config: AxiosRequestConfig, status: number, data: unknown): AxiosResponse {
  return {
    data,
    status,
    statusText: status >= 200 && status < 300 ? 'OK' : 'Error',
    headers: {},
    config: config as any,
  }
}

function error(config: AxiosRequestConfig, status: number, data: unknown) {
  const err = new Error('Static demo API error') as Error & { response?: AxiosResponse }
  err.response = response(config, status, data)
  return Promise.reject(err)
}

function normalizePath(url = '') {
  try {
    return new URL(url, window.location.origin).pathname.replace(/^\/-001/, '')
  } catch {
    return url
  }
}

if (enabled) {
  axios.defaults.adapter = async (config) => {
    const path = normalizePath(config.url)
    const method = (config.method || 'get').toLowerCase()
    const body = readBody(config.data)

    await new Promise((resolve) => window.setTimeout(resolve, 180))

    if (path === '/api/auth/login' && method === 'post') {
      const user = users[body.username]
      if (!user || user.password !== body.password) {
        return error(config, 401, { msg: 'Login failed' })
      }

      return response(config, 200, {
        token: 'static-demo-token',
        user: { username: body.username, role: user.role },
      })
    }

    if (path === '/api/auth/register' && method === 'post') {
      if (!body.username || !body.password) {
        return error(config, 400, { msg: 'Username and password are required' })
      }
      users[body.username] = { password: body.password, role: body.role || 'operator' }
      return response(config, 201, { msg: 'Success' })
    }

    if (path === '/api/history' && method === 'get') {
      return response(config, 200, history)
    }

    if (path === '/api/upload' && method === 'post') {
      const record: SignalPoint = {
        id: history.length + 1,
        lat: Number(body.lat || 29.655),
        lng: Number(body.lng || 91.125),
        alt: Number(body.alt || 3650),
        rsrp: Number(body.rsrp || -96),
        sinr: Number(body.sinr || 15),
        carrier: body.carrier || 'China Mobile',
        device_id: body.device_id || 'Device-01',
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
      }
      history.unshift(record)
      return response(config, 200, { status: 'success', id: record.id })
    }

    if (path === '/api/analysis/predict' && method === 'post') {
      const alt = Number(body.alt || 3650)
      const predicted = -88 - Math.round((alt - 3600) / 120) - Math.round(Math.random() * 8)

      return response(config, 200, {
        predicted_rsrp: predicted,
        status: predicted > -95 ? 'Normal coverage' : predicted > -105 ? 'Edge coverage' : 'Weak coverage',
        suggestions: [
          'Check nearby base-station load and handover thresholds.',
          'Adjust antenna tilt based on terrain obstruction.',
          'Add fixed-point samples on weak coverage road sections.',
        ],
        environment: { status: alt > 4500 ? 'High-altitude environment' : 'Plateau environment' },
      })
    }

    if (path === '/api/stats/comparison' && method === 'get') {
      return response(config, 200, {
        carriers: carriers.map((carrier, index) => ({
          carrier,
          avg_rsrp: -88 - index * 5,
          samples: 60 + index * 12,
        })),
      })
    }

    return error(config, 404, { msg: 'Not found' })
  }
}
