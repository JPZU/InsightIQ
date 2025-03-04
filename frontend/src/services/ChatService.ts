import { BaseService } from '@/services/BaseService'
import type { ChatResponseInterface } from '@/interfaces/ChatResponseInterface'

class ChatService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chat`

  async askQuestion(question: string): Promise<ChatResponseInterface> {
    return await this.makeRequest(ChatService.BASE_URL, 'post', { question })
  }
}

export default new ChatService()
