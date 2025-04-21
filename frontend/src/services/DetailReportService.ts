import axios from 'axios'

class DetailReportService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/detail_report`

  static get_detailed_report() {
    return axios.get(`${this.BASE_URL}/detail-report`)
  }
}

export default DetailReportService
