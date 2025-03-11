import axios, { AxiosError } from 'axios'
import type { Method } from 'axios'

export abstract class BaseService {
  protected async makeRequest(
    url: string,
    method: Method = 'get',
    body?: unknown,
    headers?: Record<string, string>,
  ): Promise<any> {
    try {
      const response = await axios({ url, method, data: body, headers })

      return response.data
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
          throw new Error('Server not available. Please try again later.')
        }
      } else {
        throw error
      }
    }
  }
}
