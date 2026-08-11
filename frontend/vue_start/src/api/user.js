import axios from 'axios'

const api = axios.create({

  baseURL: 'http://127.0.0.1:8000'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export function login(data) {

  return api.post(
    '/user/login',
    data
  )
}

export function register(data) {

  return api.post(
    '/user/register',
    data
  )
}

export function getMe() {

  return api.get('/user/me')
}
