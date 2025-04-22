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
  showResponseDetails: false
})

const filteredChats = computed(() => {
  if (!state.value.searchQuery) return state.value.chats
  return state.value.chats.filter(chat =>
    chat.name.toLowerCase().includes(state.value.searchQuery.toLowerCase()))
})

const fetchChats = async () => {
  state.value.loadingChats = true
  try {
    const response = await ChatService.getChats()
    state.value.chats = response.response
  } finally {
    state.value.loadingChats = false
  }
}

const fetchMessages = async (chatId) => {
  if (!chatId) return;
  state.value.loadingMessages = true;
  try {
    const response = await ChatService.getChatMessages(chatId);
    const messages = response.response.messages;
    console.log('Fetched messages:', messages);

    state.value.messages = messages;
    state.value.selectedChat = chatId;
    state.value.answer = null; // Reset answer when changing chats

    nextTick(() => {
      const messagesContainer = document.querySelector('.chat-messages');
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }
    });
  } catch (error) {
    console.error('Error fetching messages:', error);
  } finally {
    state.value.loadingMessages = false;
  }
};

const createChatWithName = async () => {
  try {
    const newChat = await ChatService.createChat(state.value.newChatName || "New Chat")
    state.value.chats = Array.isArray(state.value.chats) ? state.value.chats : []
    state.value.chats.unshift(newChat)
    state.value.showNewChatModal = false
    state.value.newChatName = ''
    await fetchMessages(newChat.id)
  } catch (error) {
    console.error('Error creating chat:', error)
  }
}

const submitQuestion = async () => {
  if (!state.value.question.trim()) return

  state.value.loading = true
  state.value.answer = null
  const userQuestion = state.value.question

  try {
    state.value.messages = Array.isArray(state.value.messages) ? state.value.messages : []
    state.value.messages.push({
      type: 'question',
      content: userQuestion,
      created_at: new Date().toISOString()
    })

    let response
    if (state.value.selectedChat) {
      response = await ChatService.askChat(state.value.selectedChat, userQuestion)
      if (response?.success) {
        const message = {
          type: 'response',
          content: response.response?.answer || "No response content",
          created_at: new Date().toISOString(),
          result: response.response?.result || {}
        }
        state.value.messages.push(message)
        
        // Si la respuesta contiene datos para gráficas
        if (response.response?.result?.x_axis && response.response?.result?.y_axis) {
          state.value.answer = response.response.result
        }
      }
    } else {
      response = await ChatService.askQuestion(userQuestion)
      state.value.answer = response.response
    }

    state.value.question = ''
  } catch (error) {
    const errorContent = error instanceof Error ? error.message : 'Failed to get response'
    const errorMessage = {
      type: 'response',
      content: errorContent,
      created_at: new Date().toISOString()
    }

    if (state.value.selectedChat) {
      state.value.messages.push(errorMessage)
    } else {
      state.value.answer = { error: errorContent }
    }
  } finally {
    state.value.loading = false
  }
}

const clearFields = () => {
  state.value.question = ''
  state.value.answer = null
  state.value.chartTitle = ''
}

const getButtonClass = (mode) => {
  return state.value.viewMode === mode ? 'btn-primary text-white' : 'btn-outline-primary'
}

const isValidQueryOutput = (queryOutput) => {
  return queryOutput && !queryOutput.error && Array.isArray(queryOutput) && queryOutput.length > 0
}

const toggleResponseDetails = () => {
  state.value.showResponseDetails = !state.value.showResponseDetails
}

onMounted(fetchChats)
</script>

<template>
  <div class="app-container">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-header">
        <input v-model="state.searchQuery" placeholder="Buscar chats..." class="search-input">
        <button @click="state.showNewChatModal = true" class="new-chat-btn">
          + Nuevo Chat
        </button>
      </div>
      
      <div class="chat-list">
        <div v-for="chat in filteredChats" :key="chat.id" 
             @click="fetchMessages(chat.id)"
             :class="['chat-item', { 'active': chat.id === state.selectedChat }]">
          {{ chat.name }}
        </div>
      </div>
    </div>

    <div class="chat-area">
      <div v-if="!state.selectedChat" class="empty-state">
        <div class="empty-content">
          <i class="bi bi-chat-left-text"></i>
          <h3>Selecciona un chat</h3>
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
              
              <!-- Botón para mostrar detalles de respuesta si hay datos -->
              <button v-if="message.type === 'response' && message.result && (message.result.x_axis || message.result.query_output)"
                      @click="state.answer = message.result; state.showResponseDetails = true"
                      class="details-btn">
                Ver detalles
              </button>
              
              <div class="message-time">
                {{ new Date(message.created_at).toLocaleTimeString() }}
              </div>
            </div>

            <div v-if="state.messages.length === 0" class="no-messages">
              No hay mensajes en este chat
            </div>
          </div>
        </div>

        <!-- Sección de visualización de gráficas/detalles -->
        <div v-if="state.answer && state.showResponseDetails" class="response-details">
          <div class="card">
            <h3>Detalles de la respuesta</h3>
            
            <table v-if="state.answer.input || state.answer.output || state.answer.query" class="table formatted-table table-bordered">
              <tbody>
                <tr v-if="state.answer.input">
                  <th scope="row">Input</th>
                  <td>{{ state.answer.input }}</td>
                </tr>
                <tr v-if="state.answer.output">
                  <th scope="row">Output</th>
                  <td>{{ state.answer.output }}</td>
                </tr>
                <tr v-if="state.answer.query">
                  <th scope="row">Query</th>
                  <td>{{ state.answer.query }}</td>
                </tr>
              </tbody>
            </table>

            <div class="btn-group mt-3" role="group">
              <input
                type="radio"
                class="btn-check"
                name="viewToggle"
                id="viewGraphs"
                autocomplete="off"
                v-model="state.viewMode"
                value="graphs"
              />
              <label :class="`btn ${getButtonClass('graphs')}`" for="viewGraphs"> Gráficas </label>

              <input
                type="radio"
                class="btn-check"
                name="viewToggle"
                id="viewTable"
                autocomplete="off"
                v-model="state.viewMode"
                value="table"
              />
              <label :class="`btn ${getButtonClass('table')}`" for="viewTable"> Tabla </label>
            </div>

            <div v-if="state.viewMode === 'graphs'">
              <div class="mt-3">
                <label for="chart-type">Tipo de gráfica:</label>
                <select id="chart-type" v-model="state.chartType" class="form-control">
                  <option value="bar">Barras</option>
                  <option value="pie">Pastel</option>
                  <option value="line">Línea</option>
                </select>
              </div>

              <div class="mt-3">
                <label for="chart-title">Título:</label>
                <input
                  id="chart-title"
                  v-model="state.chartTitle"
                  class="form-control"
                  placeholder="Título de la gráfica..."
                />
              </div>

              <div
                v-if="!state.answer.x_axis?.length || !state.answer.y_axis?.length"
                class="alert alert-info mt-3"
              >
                No hay datos para mostrar gráficas
              </div>

              <BarChart
                v-if="state.chartType === 'bar' && state.answer.x_axis?.length && state.answer.y_axis?.length"
                :xAxis="state.answer.x_axis"
                :yAxis="state.answer.y_axis"
                :chartTitle="state.chartTitle || 'Gráfica de Barras'"
              />
              <PieChart
                v-else-if="state.chartType === 'pie' && state.answer.x_axis?.length && state.answer.y_axis?.length"
                :xAxis="state.answer.x_axis"
                :yAxis="state.answer.y_axis"
                :chartTitle="state.chartTitle || 'Gráfica de Pastel'"
              />
              <LineChart
                v-else-if="state.chartType === 'line' && state.answer.x_axis?.length && state.answer.y_axis?.length"
                :xAxis="state.answer.x_axis"
                :yAxis="state.answer.y_axis"
                :chartTitle="state.chartTitle || 'Gráfica de Líneas'"
              />
            </div>

            <div v-else-if="state.viewMode === 'table'">
              <div v-if="isValidQueryOutput(state.answer.query_output)">
                <Table :queryOutput="state.answer.query_output" />
              </div>
              <div v-else class="alert alert-info mt-3">
                No hay datos para mostrar en tabla
              </div>
            </div>

            <button @click="state.showResponseDetails = false" class="btn btn-secondary mt-3">
              Cerrar detalles
            </button>
          </div>
        </div>

        <div class="message-input">
          <input v-model="state.question" placeholder="Escribe un mensaje..." 
                 @keyup.enter="submitQuestion" />
          <button @click="submitQuestion" :disabled="state.loading">
            <span v-if="state.loading">Enviando...</span>
            <span v-else>Enviar</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="state.showNewChatModal" class="modal">
      <div class="modal-content">
        <h3>Nuevo Chat</h3>
        <input v-model="state.newChatName" placeholder="Nombre del chat" />
        <div class="modal-actions">
          <button @click="state.showNewChatModal = false">Cancelar</button>
          <button @click="createChatWithName">Crear</button>
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
  max-width: 70%;
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

.message-time {
  font-size: 0.75rem;
  color: #666;
  text-align: right;
  margin-top: 0.25rem;
}

.details-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
}

.details-btn:hover {
  background: #f8f9fa;
}

.message-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.message-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.message-input button {
  margin-left: 0.5rem;
  padding: 0 1rem;
  background: #0395ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.response-details {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  max-height: 40vh;
  overflow-y: auto;
}

.card {
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: white;
}

.btn-group {
  margin-bottom: 1rem;
}

.btn-primary {
  background-color: #0d6efd !important;
  border-color: #0d6efd !important;
}

.btn-outline-primary {
  border: 2px solid;
  color: #0d6efd !important;
  border-color: #0d6efd !important;
  background-color: white;
}

.btn-outline-primary:hover {
  background-color: #0d6efd !important;
  color: white !important;
}

.formatted-table {
  table-layout: fixed;
  width: 100%;
  word-wrap: break-word;
}

.formatted-table th,
.formatted-table td {
  max-width: 400px;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
  gap: 0.5rem;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>