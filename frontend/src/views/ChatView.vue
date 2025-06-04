<script setup lang="ts">
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import ChatService from '@/services/ChatService'
import BarChart from '@/components/BarChart.vue'
import PieChart from '@/components/PieChart.vue'
import LineChart from '@/components/LineChart.vue'
import SidebarComponent from '@/components/layouts/SidebarComponent.vue'
import '@/assets/main.css'

type Message = {
  type: 'question' | 'response'
  content: string
  created_at: string
  response_id?: number
  rating?: number | null
  query_result?: any | null
  result?: any | null
}

type State = {
  question: string
  answer: any | null
  loading: boolean
  chartType: 'bar' | 'pie' | 'line'
  viewMode: 'graphs' | 'table'
  chats: Array<{ id: number; name: string }>
  messages: Message[]
  selectedChat: number | null
  searchQuery: string
  loadingChats: boolean
  loadingMessages: boolean
  showNewChatModal: boolean
  newChatName: string
  expandedMessages: Record<number, boolean>
  selectedMessageIndex: number | null
  selectedColumns: { x: string; y: string } | null
}

const state = ref<State>({
  question: '',
  answer: null,
  loading: false,
  chartType: 'bar',
  viewMode: 'table',
  chats: [],
  messages: [],
  selectedChat: null,
  searchQuery: '',
  loadingChats: false,
  loadingMessages: false,
  showNewChatModal: false,
  newChatName: '',
  expandedMessages: {} as Record<number, boolean>,
  selectedMessageIndex: null,
  selectedColumns: null,
})

const filteredChats = computed(() =>
  !state.value.searchQuery
    ? state.value.chats
    : state.value.chats.filter((chat) =>
        chat.name.toLowerCase().includes(state.value.searchQuery.toLowerCase()),
      ),
)

const fetchChats = async () => {
  state.value.loadingChats = true
  try {
    const res = await ChatService.getChats()
    state.value.chats = res.response || []
  } catch (error) {
    console.error('Error fetching chats:', error)
  } finally {
    state.value.loadingChats = false
  }
}

const scrollToBottom = async () => {
  await nextTick()
  const messagesContainer = document.querySelector('.chat-messages')
  if (messagesContainer) {
    messagesContainer.scrollTo({
      top: messagesContainer.scrollHeight,
      behavior: 'smooth'
    })
  }
}

const scrollToMessage = async (index: number) => {
  await nextTick()
  const messagesContainer = document.querySelector('.chat-messages')
  const messageElement = document.querySelector(`.message:nth-child(${index + 1})`)
  if (messagesContainer && messageElement) {
    // Scroll to show the top of the message
    messagesContainer.scrollTo({
      top: messageElement.getBoundingClientRect().top + messagesContainer.scrollTop - messagesContainer.getBoundingClientRect().top,
      behavior: 'smooth'
    })
  }
}

const fetchMessages = async (chatId: number) => {
  if (!chatId) return
  state.value.loadingMessages = true
  try {
    const res = await ChatService.getChatMessages(chatId)
    state.value.messages = (res.response?.messages || []).map(msg => ({
      ...msg,
      result: msg.type === 'response' && msg.query_result ? processQueryResult(msg.query_result) : null
    }))
    state.value.selectedChat = chatId
    state.value.answer = null
    state.value.expandedMessages = state.value.messages.reduce((acc, msg, index) => {
      if (msg.type === 'response' && msg.result && Object.keys(msg.result).length > 0) {
        acc[index] = true
      }
      return acc
    }, {} as Record<number, boolean>)
    
    // Wait for the DOM to update with the new messages
    await nextTick()
    // Use smooth scrolling after a small delay to ensure all content is rendered
    setTimeout(() => {
      const messagesContainer = document.querySelector('.chat-messages')
      if (messagesContainer) {
        messagesContainer.scrollTo({
          top: messagesContainer.scrollHeight,
          behavior: 'smooth'
        })
      }
    }, 100)
  } catch (error) {
    console.error('Error fetching messages:', error)
  } finally {
    state.value.loadingMessages = false
  }
}

const createChatWithName = async () => {
  if (!state.value.newChatName.trim()) {
    alert('Por favor ingresa un nombre para el chat')
    return
  }
  try {
    const res = await ChatService.createChat(state.value.newChatName)
    state.value.chats = [res.response, ...state.value.chats]
    state.value.showNewChatModal = false
    state.value.newChatName = ''
    await fetchMessages(res.response.id)
  } catch (error) {
    console.error('Error creating chat:', error)
  }
}

const hasErrorColumns = (data) => {
  if (!data || typeof data !== 'object') return false
  const keys = Object.keys(data)
  
  // Check if both error and details exist and are strings
  const hasErrorAndDetails = keys.includes('error') && 
                           keys.includes('details') && 
                           typeof data.error === 'string' && 
                           typeof data.details === 'string' &&
                           !Array.isArray(data.error) &&
                           !Array.isArray(data.details)

  return hasErrorAndDetails
}

// Add back the formatColumnName function
const formatColumnName = (name) => {
  return name
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

const processQueryResult = (result) => {
  try {
    const parsed = typeof result === 'string' ? JSON.parse(result) : result
    
    if (hasErrorColumns(parsed)) {
      console.error('Data contains error columns:', parsed)
      return {
        query_result: null,
        x_axis: [],
        y_axis: [],
        chartTitle: '',
        error: 'The response contains error information. Please try rephrasing your question.'
      }
    }

    // Check if the data is malformed (appears to be text split into columns)
    const isMalformedData = (data) => {
      if (!data || typeof data !== 'object') return false
      const keys = Object.keys(data)
      if (keys.length === 0) return false
      
      // Check if the data looks like text split into columns
      const firstKey = keys[0]
      const values = data[firstKey]
      if (!Array.isArray(values)) return false
      
      // If we have very short strings in each column, it might be malformed
      const hasShortStrings = values.some(val => 
        typeof val === 'string' && val.length <= 2
      )
      
      // If we have many columns with single characters, it's likely malformed
      const hasManySingleCharColumns = keys.length > 5 && 
        keys.every(key => Array.isArray(data[key]) && 
          data[key].every(val => typeof val === 'string' && val.length <= 2))
      
      return hasShortStrings && hasManySingleCharColumns
    }

    if (isMalformedData(parsed)) {
      console.error('Received malformed data structure:', parsed)
      return {
        query_result: null,
        x_axis: [],
        y_axis: [],
        chartTitle: '',
        error: 'The data received appears to be malformed. Please try rephrasing your question.'
      }
    }

    if (!parsed || typeof parsed !== 'object' || Object.keys(parsed).length === 0) {
      return {
        query_result: null,
        x_axis: [],
        y_axis: [],
        chartTitle: '',
        warning: 'This question does not seem to create a valid table or graph. Please try rephrasing your question.'
      }
    }

    const keys = Object.keys(parsed)
    
    // Helper function to check if a value is an array
    const isArray = (val) => Array.isArray(val)
    
    // Find first string column and first numeric column that are arrays
    const stringColumn = keys.find(key => {
      const values = parsed[key]
      if (!isArray(values) || values.length === 0) return false
      const firstValue = values[0]
      return typeof firstValue === 'string' || isNaN(Number(firstValue))
    })
    
    const numericColumn = keys.find(key => {
      const values = parsed[key]
      if (!isArray(values) || values.length === 0) return false
      const firstValue = values[0]
      return !isNaN(Number(firstValue))
    })
    
    // Use the found columns for the graph
    const xColumn = stringColumn
    const yColumn = numericColumn

    // Ensure we have valid arrays before mapping
    const x_axis = xColumn && isArray(parsed[xColumn]) ? parsed[xColumn].map(val => String(val)) : []
    const y_axis = yColumn && isArray(parsed[yColumn]) ? parsed[yColumn].map(val => Number(val)) : []
    
    // Create chart title using the selected columns
    const chartTitle = xColumn && yColumn
      ? `${formatColumnName(yColumn)} vs ${formatColumnName(xColumn)}`
      : ''

    return { 
      query_result: parsed,
      x_axis,
      y_axis,
      chartTitle,
      error: null
    }
  } catch (error) {
    console.error('Error processing query result:', error)
    return {
      query_result: null,
      x_axis: [],
      y_axis: [],
      chartTitle: '',
      error: 'Error processing the response. Please try rephrasing your question.'
    }
  }
}

const submitQuestion = async () => {
  if (!state.value.question.trim()) return
  const userQuestion = state.value.question
  state.value.loading = true
  state.value.question = ''

  state.value.messages.push({
    type: 'question',
    content: userQuestion,
    created_at: new Date().toISOString(),
  })

  await nextTick(scrollToBottom)

  try {
    const res = state.value.selectedChat
      ? await ChatService.askChat(state.value.selectedChat, userQuestion)
      : await ChatService.askQuestion(userQuestion)

    // Check if we have a valid response
    if (!res || !res.response) {
      throw new Error('Invalid response from server')
    }

    const msg = res.response
    const processedResult = msg?.query_result ? processQueryResult(msg.query_result) : null

    // Add the new message and immediately expand it if it has data
    const newMessageIndex = state.value.messages.length
    state.value.messages.push({
      type: 'response',
      content: msg?.content || 'No response content',
      created_at: new Date().toISOString(),
      result: processedResult,
      response_id: msg?.response_id || null,  // Make response_id optional
      rating: null,
    })

    // First scroll to show the top of the new message
    await scrollToMessage(newMessageIndex)

    // If the message has data, expand it after a short delay
    if (processedResult && Object.keys(processedResult).length > 0) {
      // Wait a bit before expanding to ensure the scroll to message is complete
      setTimeout(() => {
        state.value.expandedMessages[newMessageIndex] = true
        // Then scroll to bottom to show the full content
        setTimeout(() => {
          scrollToBottom()
        }, 100)
      }, 300)
    }
  } catch (error) {
    console.error('Error al enviar pregunta:', error)
    state.value.messages.push({
      type: 'response',
      content: 'Ocurrió un error al procesar tu pregunta. Por favor, intenta reformularla.',
      created_at: new Date().toISOString(),
      result: null,
      response_id: null,  // Explicitly set response_id to null for error messages
      rating: null,
    })
  } finally {
    state.value.loading = false
  }
}

const rateResponse = async (index: number, rating: number) => {
  const message = state.value.messages[index]
  if (message.rating !== null || !message.response_id) return

  try {
    await ChatService.rateResponse(message.response_id, rating)
    message.rating = rating
  } catch (err) {
    console.error('Error al calificar respuesta:', err)
    alert('Ocurrió un error al calificar la respuesta.')
  }
}

const toggleMessageDetails = (index: number) => {
  state.value.expandedMessages[index] = !state.value.expandedMessages[index]
}

const formatMessage = (content) => {
  if (!content) return ''
  
  let formatted = content.replace(/`([^`]+)`/g, '<code>$1</code>')
  
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  
  formatted = formatted.replace(/(\d+\.\s+[^\n]+)/g, '<div class="list-item">$1</div>')
  
  formatted = formatted.replace(/\n/g, '<br>')
  
  return formatted
}

onMounted(fetchChats)

// In the script setup section, expose the function to the template
defineExpose({
  hasErrorColumns
})
</script>

<template>
  <div class="app-container">
    <SidebarComponent
      :items="filteredChats"
      :selectedItemId="state.selectedChat"
      v-model:searchQuery="state.searchQuery"
      :searchPlaceholder="$t('chat.search_placeholder')"
      :newItemButtonText="$t('chat.new_chat')"
      @itemSelected="(chat) => fetchMessages(chat.id)"
      @newItemClick="state.showNewChatModal = true"
    />

    <div class="chat-area">
      <div v-if="!state.selectedChat" class="empty-state">
        <div class="empty-content">
          <i class="bi bi-chat-left-text"></i>
          <h3>{{ $t('chat.select_chat') }}</h3>
        </div>
      </div>

      <div v-else class="active-chat">
        <div class="messages-container chat-messages">
          <div v-if="state.loadingMessages" class="loading-spinner">
            <div class="spinner"></div>
          </div>

          <template v-else>
            <div
              v-for="(message, index) in state.messages"
              :key="index"
              :class="['message', message.type === 'question' ? 'user-message' : 'ai-message']"
              :id="`message-${index}`"
            >
              <div class="message-content-wrapper">
                <div class="message-content" v-if="message.type === 'question'">{{ message.content }}</div>
                <div class="message-content formatted-content" v-else v-html="formatMessage(message.content)"></div>
              </div>

              <div class="message-footer">
                <div class="message-actions">
                  <span
                    v-if="message.type === 'response' && message.result && Object.keys(message.result).length > 0"
                    @click="toggleMessageDetails(index)"
                    class="details-toggle"
                  >
                    <i :class="['bi', state.expandedMessages[index] ? 'bi-chevron-up' : 'bi-chevron-down']"></i>
                    {{ state.expandedMessages[index] ? $t('chat.hide_details') : $t('chat.show_details') }}
                  </span>

                  <div v-if="message.type === 'response' && message.response_id" class="rating-buttons">
                    <button 
                      @click="rateResponse(index, 1)" 
                      :disabled="message.rating !== null" 
                      :class="{ active: message.rating === 1 }"
                      :title="message.rating === 1 ? 'You liked this response' : 'Like this response'"
                    >
                      👍
                    </button>
                    <button 
                      @click="rateResponse(index, 0)" 
                      :disabled="message.rating !== null" 
                      :class="{ active: message.rating === 0 }"
                      :title="message.rating === 0 ? 'You disliked this response' : 'Dislike this response'"
                    >
                      👎
                    </button>
                  </div>
                </div>
              </div>

              <!-- Data details section -->
              <div v-if="message.type === 'response' && message.result && (Object.keys(message.result).length > 0 || message.result.error || message.result.warning) && state.expandedMessages[index]" 
                   class="message-details">
                <div v-if="message.result.error" class="alert alert-error">
                  {{ message.result.error }}
                </div>
                <div v-else-if="message.result.warning" class="alert alert-warning">
                  {{ message.result.warning }}
                </div>
                <template v-else-if="!hasErrorColumns(message.result.query_result)">
                  <div class="view-toggle">
                    <button
                      :class="['btn', state.viewMode === 'table' ? 'btn-primary' : 'btn-outline']"
                      @click="state.viewMode = 'table'"
                    >
                      {{ $t('chat.table') }}
                    </button>
                    <button
                      :class="['btn', state.viewMode === 'graphs' ? 'btn-primary' : 'btn-outline']"
                      @click="state.viewMode = 'graphs'"
                    >
                      {{ $t('chat.graphs') }}
                    </button>
                  </div>

                  <div v-if="state.viewMode === 'table'" class="table-container">
                    <table class="table">
                      <thead>
                        <tr>
                          <th v-for="(_, key) in message.result.query_result" :key="key">
                            {{ key }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(_, i) in message.result.query_result[Object.keys(message.result.query_result)[0]]" :key="i">
                          <td v-for="(values, key) in message.result.query_result" :key="key">
                            {{ values[i] }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div v-else class="graph-section">
                    <select v-model="state.chartType" class="form-control">
                      <option value="bar">{{ $t('chat.bar_chart') }}</option>
                      <option value="pie">{{ $t('chat.pie_chart') }}</option>
                      <option value="line">{{ $t('chat.line_chart') }}</option>
                    </select>

                    <div v-if="message.result.x_axis?.length && message.result.y_axis?.length" class="chart-container">
                      <component
                        :is="state.chartType === 'bar' ? BarChart : state.chartType === 'pie' ? PieChart : LineChart"
                        :xAxis="message.result.x_axis"
                        :yAxis="message.result.y_axis"
                        :chartTitle="message.result.chartTitle"
                        :key="state.chartType"
                      />
                    </div>
                    <div v-else class="alert">
                      {{ $t('chat.no_chart') }}
                    </div>
                  </div>
                </template>
                <div v-else class="alert alert-error">
                  The response contains error information. Please try rephrasing your question.
                </div>
              </div>
            </div>

            <div v-if="state.loading" class="message ai-message">
              <div class="message-content-wrapper">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>

            <div v-if="state.messages.length === 0" class="no-messages">
              {{ $t('chat.no_messages') }}
            </div>
          </template>
        </div>

        <div class="message-input">
          <input 
            v-model="state.question" 
            :placeholder="$t('chat.ask')" 
            @keyup.enter="submitQuestion"
            :disabled="state.loading"
          />
          <button @click="submitQuestion" :disabled="state.loading || !state.question.trim()">
            <span v-if="state.loading" class="sending-indicator">
              <i class="bi bi-arrow-repeat"></i>
              {{ $t('chat.thinking') }}
            </span>
            <span v-else>
              <i class="bi bi-send"></i>
              {{ $t('chat.send') }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="state.showNewChatModal" class="modal" @click.self="state.showNewChatModal = false">
      <div class="modal-content">
        <h3>{{ $t('chat.new_chat') }}</h3>
        <input v-model="state.newChatName" :placeholder="$t('chat.chat_name')" @keyup.enter="createChatWithName" />
        <div class="modal-actions">
          <button @click="state.showNewChatModal = false">{{ $t('chat.cancel') }}</button>
          <button @click="createChatWithName" :disabled="!state.newChatName.trim()">{{ $t('chat.create') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container { display: flex; height: 83vh; }
.chat-area { flex: 1; display: flex; flex-direction: column; }
.empty-state { display: flex; justify-content: center; align-items: center; height: 100%; }
.active-chat { display: flex; flex-direction: column; height: 100%; }
.messages-container {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  scroll-behavior: smooth;
}

.message {
  max-width: 80%;
  margin-bottom: 0;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f0f0f0;
  display: flex;
  flex-direction: column;
  width: fit-content;
  min-width: 100px;
  align-self: flex-start;
  scroll-margin-top: 1rem; /* Add scroll margin to ensure proper positioning */
}

.user-message { 
  background: #e3f2fd; 
  align-self: flex-end;
}

.message-content-wrapper {
  width: 100%;
  display: flex;
  align-items: flex-start;
}

.message-content {
  margin-bottom: 0.5rem;
  word-break: break-word;
  width: 100%;
}

.message-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  width: 100%;
}

.message-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  justify-content: flex-end;
}

.rating-buttons {
  display: flex;
  gap: 0.5rem;
}

.rating-buttons button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
  opacity: 0.6;
  font-size: 1.2rem;
}

.rating-buttons button:hover {
  opacity: 1;
  transform: scale(1.1);
}

.rating-buttons button.active {
  opacity: 1;
}

.rating-buttons button:disabled {
  cursor: default;
  opacity: 0.3;
}

.rating-buttons button:disabled.active {
  opacity: 1;
}

.details-toggle {
  color: #4a6baf;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  padding: 0.25rem 0;
  transition: color 0.2s;
}

.details-toggle:hover {
  color: #2c4a8f;
}

.details-toggle i {
  font-size: 1.1em;
  transition: transform 0.2s;
}

.message-details {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  width: 100%;
}

.message-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  background: white;
  gap: 0.5rem;
}

.message-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.message-input button {
  padding: 0 1rem;
  background: #0395ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 100px;
  justify-content: center;
}

.message-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.message-input input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.modal-content input {
  width: 100%;
  padding: 0.75rem;
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions button:last-child {
  background: #0395ff;
  color: white;
}

.loading-spinner { display: flex; justify-content: center; padding: 2rem; }
.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.view-toggle { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
.btn { padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer; }
.btn-primary { background: #0d6efd; color: white; }
.btn-outline { border: 1px solid #0d6efd; color: #0d6efd; }

.table-container { overflow-x: auto; max-width: 100%; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 0.5rem; border: 1px solid #ddd; text-align: left; }
.table th { background: #f8f9fa; }

.alert { padding: 0.5rem; border-radius: 4px; background: #e7f5ff; color: #1864ab; }
.form-control { padding: 0.375rem 0.75rem; border: 1px solid #ced4da; border-radius: 0.25rem; }

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: #f0f0f0;
  border-radius: 16px;
  width: fit-content;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #666;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.sending-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.graph-section {
  margin-top: 1rem;
}

.chart-container {
  margin-top: 1rem;
  min-height: 300px;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.details-toggle {
  color: #4a6baf;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  padding: 0.25rem 0;
  transition: color 0.2s;
}

.details-toggle:hover {
  color: #2c4a8f;
}

.details-toggle i {
  font-size: 1.1em;
  transition: transform 0.2s;
}

.table-container {
  margin-top: 1rem;
  overflow-x: auto;
  max-width: 100%;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table th,
.table td {
  padding: 0.75rem;
  text-align: left;
  border: 1px solid #e2e8f0;
}

.table th {
  background: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

.table tr:nth-child(even) {
  background: #f8fafc;
}

.table tr:hover {
  background: #f1f5f9;
}

.column-selectors,
.selector-group {
  display: none;
}

.alert-detail {
  font-size: 0.9em;
  margin-top: 0.5rem;
  color: #4a5568;
}

.alert-warning {
  background-color: #fff3cd;
  color: #856404;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.alert-error {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}
</style>
