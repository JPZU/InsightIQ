import { BaseService } from '@/services/BaseService'

interface LoginResponse {
  success: boolean
  response?: {
    access_token: string
    token_type: string
  }
  message?: string
}

interface TokenData {
  access_token: string
  token_type: string
}

interface User {
  id: number
  username: string
  email: string
}

class AuthService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/auth`

  public async login(username: string, password: string): Promise<boolean> {
    try {
      const requestBody = new URLSearchParams()
      requestBody.append('username', username)
      requestBody.append('password', password)

      const response = (await this.makeRequest(
        `${AuthService.BASE_URL}/token`,
        'post',
        requestBody.toString(),
        { 'Content-Type': 'application/x-www-form-urlencoded' },
      )) as TokenData

      if (response && response.access_token) {
        localStorage.setItem('access_token', response.access_token)
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  public async refreshToken(): Promise<boolean> {
    try {
      const response = (await this.makeRequest(
        `${AuthService.BASE_URL}/refresh`,
        'post',
      )) as TokenData

      if (response && response.access_token) {
        localStorage.setItem('access_token', response.access_token)
        return true
      }
      return false
    } catch (error) {
      console.error('Token refresh error:', error)
      return false
    }
  }

  public async logout(): Promise<boolean> {
    try {
      await this.makeRequest(`${AuthService.BASE_URL}/logout`, 'post')
      localStorage.removeItem('access_token')
      return true
    } catch (error) {
      console.error('Logout error:', error)
      localStorage.removeItem('access_token')
      return false
    }
  }

  public isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  }

  public getToken(): string | null {
    return localStorage.getItem('access_token')
  }
}

export default new AuthService()
