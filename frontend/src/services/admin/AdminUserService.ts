import { BaseService } from '@/services/BaseService'

interface UserInfo {
  general_metrics: {
    total_users: number
    total_admins: number
    total_questions_asked: number
  }
  users_info: Array<{
    name: string
    email: string
    role: 'user' | 'admin'
    questions_asked: number
  }>
}

interface UserDetails {
  id: number
  full_name: string
  username: string
  email: string
  role: 'user' | 'admin'
  created_at: string
  updated_at: string
}

interface AdminUserUpdate {
  full_name?: string
  username?: string
  email?: string
  password?: string
  role?: 'user' | 'admin'
}

interface BaseResponse<T = any> {
  success?: boolean
  message?: string
  response?: T
}

class AdminUserService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/admin/users`

  async listAllUsers(): Promise<BaseResponse<UserInfo>> {
    return (await this.makeRequest(
      AdminUserService.BASE_URL,
      'get'
    )) as BaseResponse<UserInfo>
  }

  async getUserDetails(userId: number): Promise<BaseResponse<UserDetails>> {
    return (await this.makeRequest(
      `${AdminUserService.BASE_URL}/${userId}`,
      'get'
    )) as BaseResponse<UserDetails>
  }

  async updateUser(
    userId: number,
    userData: AdminUserUpdate
  ): Promise<BaseResponse> {
    return (await this.makeRequest(
      `${AdminUserService.BASE_URL}/${userId}`,
      'put',
      userData
    )) as BaseResponse
  }

  async deleteUser(userId: number): Promise<BaseResponse> {
    return (await this.makeRequest(
      `${AdminUserService.BASE_URL}/${userId}`,
      'delete'
    )) as BaseResponse
  }

  async promoteToAdmin(userId: number): Promise<BaseResponse> {
    return this.updateUser(userId, { role: 'admin' })
  }
}

export default new AdminUserService()