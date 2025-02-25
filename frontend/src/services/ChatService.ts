import axios from 'axios'

class ChatService {
  private static readonly BASE_URL = `${import.meta.env.VITE_API_URL}/chat`

  async askQuestion(question: string): Promise<any> {
    const response = await axios.post(ChatService.BASE_URL, { question })
    return response.data.response
  }
}

export default new ChatService()
