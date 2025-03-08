import axios from 'axios'

class DashboardService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/dashboard`
}

export default {
  getSchema() {
    return axios.get(`${DashboardService.BASE_URL}/`)
  },

  getAnalysis() {
    return axios.get(`${DashboardService.BASE_URL}/analysis`)
  },
}
