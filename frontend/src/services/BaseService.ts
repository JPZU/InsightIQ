// BaseService.ts
import axios, { AxiosError } from 'axios'
import type { Method } from 'axios'

export abstract class BaseService {
  protected async makeRequest(
    url: string,
    method: Method = 'get',
    body?: unknown,
    headers?: Record<string, string>,
  ): Promise<unknown> {
    try {
      // Get token from localStorage
      const token = localStorage.getItem('access_token')

      // Create default headers
      const defaultHeaders: Record<string, string> = {
        'Content-Type': 'application/json',
      }

      // Add authorization token if available
      if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`
      }

      // Merge with custom headers
      const finalHeaders = { ...defaultHeaders, ...headers }

      console.log(`Making ${method.toUpperCase()} request to:`, url)

      const response = await axios({
        url,
        method,
        data: body,
        headers: finalHeaders,
        withCredentials: true, // Important for cookies if using them
      })

      return response.data
    } catch (error) {
      console.error('Request error:', error)

      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          console.log('Authentication error - redirecting to login')
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }

        if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
          throw new Error('Server not available. Please try again later.')
        }
      }

      throw error
    }
  }
}
