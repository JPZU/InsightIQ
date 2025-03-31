import axios from 'axios'

class SyntheticDataService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chat`
}

////
export default {
  uploadDatabase(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return axios.post(`${SyntheticDataService.BASE_URL}/upload/`, formData)
  },

  getSchema(tableName: string) {
    return axios.get(`${SyntheticDataService.BASE_URL}/schema/${tableName}`)
  },

  generateSyntheticData(tableName: string, numRecords: number) {
    return axios.post(`${SyntheticDataService.BASE_URL}/generate/`, { tableName, numRecords })
  },
}
