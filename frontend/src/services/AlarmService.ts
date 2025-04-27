import axios from 'axios'
import { BaseService } from '@/services/BaseService'

class AlarmService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/alarm_management`

  static async listAlarms() {
    const response = await axios.get(`${this.BASE_URL}/list`)
    return response.data
  }

  static async deleteAlarm(id: number) {
    return await axios.delete(`${this.BASE_URL}/delete/${id}`)
  }

  static async createAlarm(userInput: string) {
    return await axios.post(`${this.BASE_URL}/create`, null, {
      params: { user_input: userInput },
    })
  }

  static async updateAlarm(id: number, updatedData: any) {
    return await axios.patch(`${this.BASE_URL}/update/${id}`, updatedData)
  }

  static async checkAlarms() {
    return await axios.get(`${this.BASE_URL}/check_alarm`, {
      params: { table_name: 'inventario' },
    })
  }
}

export default AlarmService
