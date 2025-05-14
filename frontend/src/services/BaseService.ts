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
        withCredentials: false, // Changed to false to avoid CORS issues with wildcard origins
      })

      return response.data
    } catch (error) {
      console.error('Request error:', error)

      if (error instanceof AxiosError) {
        // Handle specific error cases
        if (error.response) {
          // The server responded with a status code outside of the 2xx range
          console.log('Server error:', error.response.status, error.response.data)
          
          if (error.response.status === 401) {
            console.log('Authentication error - redirecting to login')
            localStorage.removeItem('access_token')
            window.location.href = '/login'
            throw new Error('Authentication failed. Please log in again.')
          }
          
          // Return the error response from the server if available
          return {
            success: false,
            message: error.response.data?.message || `Error: ${error.response.status}`
          }
        } else if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
          return {
            success: false,
            message: 'Server not available. Please try again later.'
          }
        }
      }

      // For any other errors, return a generic error response
      return {
        success: false,
        message: error instanceof Error ? error.message : 'An unexpected error occurred'
      }
    }
  }
}