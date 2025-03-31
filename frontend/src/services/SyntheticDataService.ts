import axios from 'axios'

class SyntheticDataService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chat`

  static uploadDatabase(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return axios.post(`${this.BASE_URL}/upload/`, formData) // ✅ Using 'this' instead of class name
  }

  static getSchema(tableName: string) {
    return axios.get(`${this.BASE_URL}/schema/${tableName}`) // ✅ Added 'static'
  }

  static generateSyntheticData(tableName: string, numRecords: number) {
    return axios.post(`${this.BASE_URL}/generate/`, { tableName, numRecords }) // ✅ Added 'static'
  }
}

export default SyntheticDataService
