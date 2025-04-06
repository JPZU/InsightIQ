import axios from 'axios'
import { BaseService } from '@/services/BaseService'

class FileManagerService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/file_manager`
}

export default {
  uploadCSV(file: File, tableName: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('table_name', tableName)

    return axios.post(`${FileManagerService.BASE_URL}/upload/csv/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  uploadExcel(file: File, tableName: string, sheetName: number = 0) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('table_name', tableName)
    formData.append('sheet_name', sheetName.toString())

    return axios.post(`${FileManagerService.BASE_URL}/upload/excel/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
