import { BaseService } from '@/services/BaseService'

interface User {
  id: number
  full_name: string
  username: string
  email: string
  created_at: string
}

interface UserCreate {
  full_name: string
  username: string
  email: string
  password: string
}

interface UserUpdate {
  full_name?: string
  email?: string
  password?: string
}

interface BaseResponse<T = any> {
  success: boolean
  message?: string
  response?: T
}

class UserService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/users`

  async register(userData: UserCreate): Promise<BaseResponse<User>> {
    return (await this.makeRequest(
      UserService.BASE_URL,
      'post',
      userData
    )) as BaseResponse<User>
  }

  async getMyProfile(): Promise<BaseResponse<User>> {
    return (await this.makeRequest(
      `${UserService.BASE_URL}/me`,
      'get'
    )) as BaseResponse<User>
  }

  async updateProfile(userData: UserUpdate): Promise<BaseResponse> {
    return (await this.makeRequest(
      `${UserService.BASE_URL}/me`,
      'put',
      userData
    )) as BaseResponse
  }

  async deleteAccount(): Promise<BaseResponse> {
    return (await this.makeRequest(
      `${UserService.BASE_URL}/me`,
      'delete'
    )) as BaseResponse
  }
}

export default new UserService()
