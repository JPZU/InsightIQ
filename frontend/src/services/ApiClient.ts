import axios from 'axios'
import i18n from '@/locales'


const ApiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})


ApiClient.interceptors.request.use(config => {
  const lang = i18n.global.locale
  config.headers['accept-language'] = lang
  return config
})

export default ApiClient
