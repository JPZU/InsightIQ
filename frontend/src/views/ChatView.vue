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
  newChatName: ''
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
        state.value.messages.push({
          type: 'response',
          content: response.response?.answer || "No response content",
          created_at: new Date().toISOString(),
          result: response.response?.result || {}
        })
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

onMounted(fetchChats)
</script>

<template>
  <div class="app-container">
    <!-- Sidebar simplificada -->
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
        <div class="messages-container">
          <div v-if="state.loadingMessages" class="loading-spinner">
            <div class="spinner"></div>
          </div>

          <div v-else>
            <div v-for="(message, index) in state.messages" :key="index" 
                 :class="['message', message.type === 'question' ? 'user-message' : 'ai-message']">
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">
                {{ new Date(message.created_at).toLocaleTimeString() }}
              </div>
            </div>

            <div v-if="state.messages.length === 0" class="no-messages">
              No hay mensajes en este chat
            </div>
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
/* Estilos simplificados */
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

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
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
