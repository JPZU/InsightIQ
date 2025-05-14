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

  static uploadGoogleSheets(url: string, tableName: string) {
    console.log('Uploading Google Sheets:', url, tableName)

      const formData = new FormData();
      formData.append('table_name', tableName);
      formData.append('url', url);

      return ApiClient.post(`${this.BASE_URL}/upload/google-sheet/`, formData, {
          headers: {
              'Content-Type': 'multipart/form-data',
          },
      });
  }

  static updateGoogleSheets() {
    return ApiClient.post(`${this.BASE_URL}/update/google-sheets`)
  }

  static getTables() {
    return ApiClient.get(`${this.BASE_URL}/tables/`)
  }

  static getTableInfo(tableName: string) {
    return ApiClient.get(`${this.BASE_URL}/tables/${tableName}/info`)
  }

  static getAllTableData(tableName: string) {
    return ApiClient.get(`${this.BASE_URL}/tables/${tableName}/data`)
  }

  static deleteTable(tableName: string) {
    return ApiClient.delete(`${this.BASE_URL}/tables/${tableName}`)
  }

  static updateTable(tableName: string, file: File, replace: boolean = false) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('replace', replace.toString())

    return ApiClient.put(`${this.BASE_URL}/tables/${tableName}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
}

export default FileManagerService
