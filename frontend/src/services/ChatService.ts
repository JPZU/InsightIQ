import { BaseService } from '@/services/BaseService'
import type { ChatResponseInterface } from '@/interfaces/ChatResponseInterface'

interface Chat {
  id: number
  name: string
  user_id: number
}

interface Message {
  id: number
  question: string
  response: string
  created_at: string
}

interface ChatListResponse {
  id: number
  name: string
}

interface ChatMessagesResponse {
  chat_id: number
  messages: Message[]
}

interface AskChatResponse {
  answer: string
  result: any
}

class ChatService extends BaseService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chats`

  async askQuestion(question: string): Promise<ChatResponseInterface> {
    return await this.makeRequest(ChatService.BASE_URL, 'post', { question }) as ChatResponseInterface
  }

  async getChats(): Promise<ChatListResponse[]> {
    return await this.makeRequest(ChatService.BASE_URL, 'get') as ChatListResponse[]
  }

  async createChat(name: string = "New Chat"): Promise<{ id: number, name: string }> {
    return await this.makeRequest(ChatService.BASE_URL, 'post', { name: name }) as { id: number, name: string }
  }

  async getChatMessages(chatId: number): Promise<ChatMessagesResponse> {
    return await this.makeRequest(`${ChatService.BASE_URL}/${chatId}`, 'get') as ChatMessagesResponse
  }

  async askChat(chatId: number, question: string): Promise<AskChatResponse> {
    return await this.makeRequest(
      `${ChatService.BASE_URL}/${chatId}`,
      'post',
      { question: question }
    ) as AskChatResponse
  }

  async updateChatName(chatId: number, newName: string): Promise<{ success: boolean, message: string }> {
    return await this.makeRequest(
      `${ChatService.BASE_URL}/${chatId}`,
      'put',
      { new_name: newName }
    ) as { success: boolean, message: string }
  }

  async deleteChat(chatId: number): Promise<{ success: boolean, message: string }> {
    return await this.makeRequest(
      `${ChatService.BASE_URL}/${chatId}`,
      'delete'
    ) as { success: boolean, message: string }
  }

  async clearChatMessages(chatId: number): Promise<{ success: boolean, message: string }> {
    return await this.makeRequest(
      `${ChatService.BASE_URL}/${chatId}/clear`,
      'delete'
    ) as { success: boolean, message: string }
  }
}

export default new ChatService()
