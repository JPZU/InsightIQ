import axios from 'axios'

class DetailReportService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/detail_report`

  static getInventorySummary() {
    return axios.get(`${this.BASE_URL}/inventory_summary`)
  }

  static getTurnoverAnalysisByRegion() {
    return axios.get(`${this.BASE_URL}/turnover_analysis_by_region`)
  }

  static getRestockRecommendations() {
    return axios.get(`${this.BASE_URL}/restock_recommendations`)
  }
}

export default DetailReportService
