<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import ChatService from '@/services/ChatService'
import BarChart from '@/components/BarChart.vue'
import PieChart from '@/components/PieChart.vue'
import LineChart from '@/components/LineChart.vue'
import Table from '@/components/Table.vue'
import '@/assets/main.css'

const state = ref({
  question: '',
  answer: null,
  loading: false,
  chartType: 'bar',
  viewMode: 'graphs',
  chartTitle: '',
  chats: [],
  messages: [],
  selectedChat: null,
  searchQuery: '',
  loadingChats: false,
  loadingMessages: false,
  showNewChatModal: false,
  newChatName: '',
  expandedMessages: {} // Nuevo estado para controlar qué mensajes tienen gráficas expandidas
})

const filteredChats = computed(() =>
  !state.value.searchQuery
    ? state.value.chats
    : state.value.chats.filter(chat =>
      chat.name.toLowerCase().includes(state.value.searchQuery.toLowerCase()))
)

const fetchChats = async () => {
  state.value.loadingChats = true
  const res = await ChatService.getChats()
  state.value.chats = res.response || []
  state.value.loadingChats = false
}

const fetchMessages = async (chatId) => {
  if (!chatId) return
  state.value.loadingMessages = true

  const res = await ChatService.getChatMessages(chatId)
  state.value.messages = res.response?.messages || []
  state.value.selectedChat = chatId
  state.value.answer = null

  // Reset expanded messages cuando cambiamos de chat
  state.value.expandedMessages = {}

  nextTick(() => {
    scrollToBottom()
  })

  state.value.loadingMessages = false
}

const createChatWithName = async () => {
  if (!state.value.newChatName.trim()) return alert('Por favor ingresa un nombre para el chat')

  const res = await ChatService.createChat(state.value.newChatName)
  const newChat = res.response
  state.value.chats = [newChat, ...state.value.chats]
  state.value.showNewChatModal = false
  state.value.newChatName = ''
  await fetchMessages(newChat.id)
}

const processQueryResult = (result, content) => {
  const parsed = typeof result === 'string' ? JSON.parse(result) : result;

  if (parsed && Object.keys(parsed).length > 0) {
    const keys = Object.keys(parsed);
    let x_axis = [];
    let y_axis = [];
    let chartTitle = '';

    if (keys.length === 1) {
      x_axis = parsed[keys[0]] || [];
      chartTitle = `Distribución de ${keys[0]}`;
    } else if (keys.length >= 2) {
      x_axis = parsed[keys[0]] || [];
      y_axis = parsed[keys[1]] || [];
      chartTitle = `${keys[1]} vs ${keys[0]}`;
    }

    return {
      content,
      query_result: parsed,
      x_axis,
      y_axis,
      chartTitle
    };
  }
  return null;
};

const submitQuestion = async () => {
  if (!state.value.question.trim()) return

  const userQuestion = state.value.question
  state.value.loading = true
  state.value.question = ''

  // Agregar pregunta del usuario
  state.value.messages.push({
    type: 'question',
    content: userQuestion,
    created_at: new Date().toISOString()
  })

  // Desplazar hacia abajo después de agregar pregunta
  await nextTick()
  scrollToBottom()

  let res
  try {
    if (state.value.selectedChat) {
      res = await ChatService.askChat(state.value.selectedChat, userQuestion)
    } else {
      res = await ChatService.askQuestion(userQuestion)
    }

    const msg = res.response
    const processedResult = msg?.query_result ? processQueryResult(msg.query_result, msg.content) : null

    const message = {
      type: 'response',
      content: msg?.content || 'No response content',
      created_at: new Date().toISOString(),
      result: processedResult || {}
    }

    state.value.messages.push(message)

    // Desplazar hacia abajo después de recibir respuesta
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error al enviar pregunta:', error)
    state.value.messages.push({
      type: 'response',
      content: 'Ocurrió un error al procesar tu pregunta',
      created_at: new Date().toISOString(),
      result: {}
    })
  } finally {
    state.value.loading = false
  }
}

const getButtonClass = (mode) =>
  state.value.viewMode === mode ? 'btn-primary text-white' : 'btn-outline-primary'

// Función para desplazar al final del chat
const scrollToBottom = () => {
  const messagesContainer = document.querySelector('.chat-messages')
  if (messagesContainer) {
    messagesContainer.scrollTop = messagesContainer.scrollHeight
  }
}

// Función para alternar la visualización de gráficas en un mensaje
const toggleMessageDetails = async (index) => {
  state.value.expandedMessages = {
    ...state.value.expandedMessages,
    [index]: !state.value.expandedMessages[index]
  }

  // Desplazar hacia abajo después de expandir/contraer
  await nextTick()
  scrollToBottom()
}

onMounted(() => {
  fetchChats()
})
</script>

<template>
  <div class="app-container">
    <div class="sidebar">
      <div class="sidebar-header">
        <input v-model="state.searchQuery" :placeholder="$t('chat.search_placeholder')" class="search-input" />
        <button @click="state.showNewChatModal = true" class="new-chat-btn">{{ $t('chat.new_chat') }}</button>
      </div>

      <div class="chat-list">
        <div v-for="chat in filteredChats" :key="chat.id" @click="fetchMessages(chat.id)"
          :class="['chat-item', { active: chat.id === state.selectedChat }]">
          {{ chat.name }}
        </div>
      </div>
    </div>

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

          <div v-else>
            <div v-for="(message, index) in state.messages" :key="index"
              :class="['message', message.type === 'question' ? 'user-message' : 'ai-message']">
              <div class="message-content">{{ message.content }}</div>

              <div v-if="message.type === 'response' && state.expandedMessages[index] && message.result" class="message-graphs">
                <div class="btn-group mt-2 mb-2" role="group">
                  <input type="radio" class="btn-check" name="viewToggle" :id="'viewGraphs' + index" autocomplete="off"
                    v-model="state.viewMode" value="graphs" />
                  <label :class="`btn btn-sm ${getButtonClass('graphs')}`" :for="'viewGraphs' + index">{{ $t('chat.graphs') }}</label>

                  <input type="radio" class="btn-check" name="viewToggle" :id="'viewTable' + index" autocomplete="off"
                    v-model="state.viewMode" value="table" />
                  <label :class="`btn btn-sm ${getButtonClass('table')}`" :for="'viewTable' + index">{{ $t('chat.table') }}</label>
                </div>

                <div v-if="state.viewMode === 'graphs'">
                  <select v-model="state.chartType" class="form-control form-control-sm mb-2">
                    <option value="bar">{{ $t('chat.bar_chart') }}</option>
                    <option value="pie">{{ $t('chat.pie_chart') }}</option>
                    <option value="line">{{ $t('chat.line_chart') }}</option>
                  </select>

                  <div v-if="message.result.x_axis?.length && message.result.y_axis?.length">
                    <BarChart v-if="state.chartType === 'bar'" :xAxis="message.result.x_axis"
                      :yAxis="message.result.y_axis" :chartTitle="message.result.chartTitle || $t('chat.bar_chart')" />
                    <PieChart v-else-if="state.chartType === 'pie'" :xAxis="message.result.x_axis"
                      :yAxis="message.result.y_axis" :chartTitle="message.result.chartTitle || $t('chat.pie_chart')" />
                    <LineChart v-else-if="state.chartType === 'line'" :xAxis="message.result.x_axis"
                      :yAxis="message.result.y_axis" :chartTitle="message.result.chartTitle || $t('chat.line_chart')" />
                  </div>
                  <div v-else class="alert alert-info p-2">
                    {{ $t('chat.no_chart') }}
                  </div>
                </div>

                <div v-else-if="state.viewMode === 'table'">
                  <div class="table-responsive">
                    <table class="table table-sm table-bordered">
                      <thead>
                        <tr>
                          <th v-for="(value, key) in message.result.query_result" :key="key">{{ key }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(_, i) in message.result.query_result[Object.keys(message.result.query_result)[0]]"
                          :key="i">
                          <td v-for="(values, key) in message.result.query_result" :key="key">
                            {{ values[i] }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <div class="message-footer">
                <button v-if="message.type === 'response' && message.result && Object.keys(message.result).length > 0"
                  @click="toggleMessageDetails(index)" class="details-btn">
                  {{ state.expandedMessages[index] ? $t('chat.hide_details') : $t('chat.show_details') }}
                </button>

                <div class="message-time">
                  {{ new Date(message.created_at).toLocaleTimeString() }}
                </div>
              </div>
            </div>

            <div v-if="state.messages.length === 0" class="no-messages">{{ $t('chat.no_messages') }}</div>
          </div>
        </div>

        <div class="message-input">
          <input v-model="state.question" :placeholder="$t('chat.ask')" @keyup.enter="submitQuestion" />
          <button @click="submitQuestion" :disabled="state.loading">
            <span v-if="state.loading">{{ $t('chat.sending') }}</span>
            <span v-else>{{ $t('chat.send') }}</span>
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
.app-container {
  display: flex;
  height: 83vh;
}

.sidebar {
  width: 280px;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.new-chat-btn {
  width: 100%;
  padding: 0.5rem;
  background: #0395ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
}

.chat-item {
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.chat-item:hover {
  background: #f5f5f5;
}

.chat-item.active {
  background: #e3f2fd;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.active-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.message {
  max-width: 80%;
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  position: relative;
}

.user-message {
  background: #e3f2fd;
  margin-left: auto;
}

.ai-message {
  background: #f0f0f0;
  margin-right: auto;
}

.message-content {
  margin-bottom: 0.5rem;
}

.message-graphs {
  background: white;
  border-radius: 8px;
  padding: 10px;
  margin-top: 8px;
  margin-bottom: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-height: 450px;
  overflow: auto;
}

.message-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.message-time {
  font-size: 0.75rem;
  color: #666;
}

.details-btn {
  background: none;
  border: none;
  color: #4a6baf;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 2px 5px;
}

.details-btn:hover {
  text-decoration: underline;
}

.message-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.message-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.message-input button {
  padding: 0 1rem;
  background: #0395ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message-input button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
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
  margin-top: 1rem;
  gap: 0.5rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions button:first-child {
  background: #f0f0f0;
}

.modal-actions button:last-child {
  background: #0395ff;
  color: white;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Estilos para los botones de gráficas/tabla */
.btn-group {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}

.btn-primary {
  background-color: #0d6efd;
  color: white;
}

.btn-outline-primary {
  background-color: white;
  color: #0d6efd;
  border: 1px solid #0d6efd;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: white;
}

/* Estilos para tablas */
.table-responsive {
  overflow-x: auto;
  max-width: 100%;
}

.table {
  width: 100%;
  border-collapse: collapse;
  max-height: 400px;
  overflow: auto;
  display: block;
}

.table th,
.table td {
  padding: 0.5rem;
  border: 1px solid #ddd;
  text-align: left;
}

.table th {
  background-color: #f8f9fa;
}

.table-sm th,
.table-sm td {
  padding: 0.3rem;
}

/* Estilos para alertas */
.alert {
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.alert-info {
  background-color: #e7f5ff;
  color: #1864ab;
  border: 1px solid #d0ebff;
}

/* Estilos para select e inputs */
.form-control {
  padding: 0.375rem 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.form-control-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>