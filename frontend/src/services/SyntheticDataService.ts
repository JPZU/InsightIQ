import axios from 'axios'
import ApiClient from '@/services/ApiClient'

class SyntheticDataService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chat`

  static uploadDatabase(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post(`${this.BASE_URL}/upload/`, formData)
  }

  static getSchema(tableName: string) {
    return ApiClient.get(`${this.BASE_URL}/schema/${tableName}`)
  }

  static generateSyntheticData(tableName: string, numRecords: number) {
    return ApiClient.post(`${this.BASE_URL}/generate/`, { tableName, numRecords })
  }
}

export default SyntheticDataService
