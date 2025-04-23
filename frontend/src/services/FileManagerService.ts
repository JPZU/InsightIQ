import ApiClient from '@/services/ApiClient'
import { BaseService } from '@/services/BaseService'

class FileManagerService extends BaseService {
  private static readonly BASE_URL = '/file_manager'

  static uploadCSV(file: File, tableName: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('table_name', tableName)

    return ApiClient.post(`${this.BASE_URL}/upload/csv/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }

  static uploadExcel(file: File, tableName: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('table_name', tableName)

    return ApiClient.post(`${this.BASE_URL}/upload/excel/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
}

export default FileManagerService
