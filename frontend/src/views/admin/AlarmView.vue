<script setup>
import { ref, computed, reactive, onMounted, nextTick } from 'vue'
import AlarmService from '@/services/AlarmService'

const state = reactive({
  alarms: [],
  selectedAlarm: null,
  creatingNewAlarm: false,
  newAlarmInput: '',
  searchQuery: '',
  loading: false,
  loadingAlarms: false,
  successMessage: '',
  errorMessage: '',
  showNewAlarmModal: false,
  newManualAlarm: {
    table_name: '',
    field: '',
    condition: '',
    threshold: '',
    description: '',
  },
})

const filteredAlarms = computed(() =>
  !state.searchQuery
    ? state.alarms
    : state.alarms.filter(
        (alarm) =>
          alarm.table_name.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          alarm.field.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          alarm.description.toLowerCase().includes(state.searchQuery.toLowerCase()),
      ),
)

const fetchAlarms = async () => {
  state.loadingAlarms = true
  try {
    const alarms = await AlarmService.listAlarms()
    state.alarms = alarms || []
  } catch (error) {
    console.error('Error fetching alarms:', error)
  } finally {
    state.loadingAlarms = false
  }
}

const selectAlarm = async (id) => {
  state.loading = true
  state.creatingNewAlarm = false
  state.successMessage = ''
  state.errorMessage = ''

  try {
    const found = state.alarms.find((a) => a.id === id)
    if (found) {
      // Crear una copia para no modificar directamente el objeto
      state.selectedAlarm = JSON.parse(JSON.stringify(found))
    } else {
      console.error('Alarm not found')
    }
  } catch (error) {
    console.error('Error selecting alarm:', error)
  } finally {
    state.loading = false
  }
}

const updateAlarm = async () => {
  if (!state.selectedAlarm) return

  state.loading = true
  state.successMessage = ''
  state.errorMessage = ''

  try {
    const { id, ...data } = state.selectedAlarm
    await AlarmService.updateAlarm(id, data)

    // Actualizar la alarma en la lista local
    const index = state.alarms.findIndex((a) => a.id === id)
    if (index !== -1) {
      state.alarms[index] = { ...state.selectedAlarm }
    }

    state.successMessage = 'Alarma actualizada correctamente'
  } catch (error) {
    console.error('Error updating alarm:', error)
    state.errorMessage = 'Error al actualizar la alarma'
  } finally {
    state.loading = false
  }
}

const createAlarm = async () => {
  if (!state.newAlarmInput.trim()) {
    state.errorMessage = 'Por favor ingresa una descripción para la alarma'
    return
  }

  state.loading = true
  state.successMessage = ''
  state.errorMessage = ''

  try {
    await AlarmService.createAlarm(state.newAlarmInput)
    state.successMessage = 'Alarma creada correctamente'
    state.newAlarmInput = ''

    // Recargar la lista de alarmas
    await fetchAlarms()
    state.creatingNewAlarm = false
  } catch (error) {
    console.error('Error creating alarm:', error)
    state.errorMessage = 'Error al crear la alarma'
  } finally {
    state.loading = false
  }
}

const deleteSelectedAlarm = async () => {
  if (!state.selectedAlarm) return

  if (!confirm('¿Estás seguro de eliminar esta alarma?')) return

  state.loading = true

  try {
    await AlarmService.deleteAlarm(state.selectedAlarm.id)

    // Eliminar de la lista local
    state.alarms = state.alarms.filter((a) => a.id !== state.selectedAlarm.id)
    state.selectedAlarm = null
    state.successMessage = 'Alarma eliminada correctamente'
  } catch (error) {
    console.error('Error deleting alarm:', error)
    state.errorMessage = 'Error al eliminar la alarma'
  } finally {
    state.loading = false
  }
}

const cancelEdit = () => {
  state.selectedAlarm = null
  state.successMessage = ''
  state.errorMessage = ''
}

const cancelCreate = () => {
  state.creatingNewAlarm = false
  state.newAlarmInput = ''
  state.successMessage = ''
  state.errorMessage = ''
}

const startNaturalLanguageCreate = () => {
  state.showNewAlarmModal = false
  state.selectedAlarm = null
  state.creatingNewAlarm = true
}

const startManualCreate = () => {
  state.showNewAlarmModal = false
  state.selectedAlarm = {
    id: 0, // Temporal para modo creación
    table_name: '',
    field: '',
    condition: '',
    threshold: '',
    description: '',
  }
  state.creatingNewAlarm = false
}

onMounted(() => {
  fetchAlarms()
})
</script>

<template>
  <div class="app-container">
    <!-- Sidebar to list alarms -->
    <div class="sidebar">
      <div class="sidebar-header">
        <input v-model="state.searchQuery" placeholder="Search alarms..." class="search-input" />
        <button @click="state.showNewAlarmModal = true" class="new-alarm-btn">
          + New Alarm
        </button>
      </div>

      <div class="alarm-list">
        <div v-if="state.loadingAlarms" class="loading-spinner">
          <div class="spinner"></div>
        </div>
        <div v-else-if="state.alarms.length === 0" class="empty-list">
          No alarms registered
        </div>
        <div
          v-for="alarm in filteredAlarms"
          :key="alarm.id"
          @click="selectAlarm(alarm.id)"
          :class="['alarm-item', { active: alarm.id === state.selectedAlarm?.id }]"
        >
          <div class="alarm-item-title">{{ alarm.table_name }} - {{ alarm.field }}</div>
          <div class="alarm-item-subtitle">{{ alarm.condition }} {{ alarm.threshold }}</div>
        </div>
      </div>
    </div>

    <!-- Main area to edit or create alarms -->
    <div class="main-area">
      <!-- Empty state when no alarm is selected -->
      <div v-if="!state.selectedAlarm && !state.creatingNewAlarm" class="empty-state">
        <div class="empty-content">
          <i class="bi bi-bell"></i>
          <h3>Select an alarm or create a new one</h3>
        </div>
      </div>

      <!-- Form to edit existing alarm -->
      <div v-else-if="state.selectedAlarm && !state.creatingNewAlarm" class="alarm-form">
        <div class="form-header">
          <h2 class="text-2xl font-bold mb-4">Edit Alarm</h2>
          <div class="form-actions">
            <button @click="deleteSelectedAlarm" class="btn-delete">Delete</button>
          </div>
        </div>

        <form @submit.prevent="updateAlarm" class="space-y-4">
          <div>
            <label class="label">Table Name</label>
            <input v-model="state.selectedAlarm.table_name" class="input" />
          </div>

          <div>
            <label class="label">Field</label>
            <input v-model="state.selectedAlarm.field" class="input" />
          </div>

          <div>
            <label class="label">Condition</label>
            <input v-model="state.selectedAlarm.condition" class="input" />
          </div>

          <div>
            <label class="label">Threshold</label>
            <input v-model="state.selectedAlarm.threshold" class="input" />
          </div>

          <div>
            <label class="label">Description</label>
            <textarea
              v-model="state.selectedAlarm.description"
              rows="3"
              class="input textarea"
            ></textarea>
          </div>

          <div class="form-buttons">
            <button type="button" class="btn-cancel" @click="cancelEdit">Cancel</button>
            <button type="submit" class="btn-save" :disabled="state.loading">
              {{ state.loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Form to create new alarm -->
      <div v-else-if="state.creatingNewAlarm" class="alarm-form">
        <div class="form-header">
          <h2 class="text-2xl font-bold mb-4">Create Alarm</h2>
        </div>

        <form @submit.prevent="createAlarm" class="space-y-4">
          <label class="label">Natural Language Description</label>
          <textarea
            v-model="state.newAlarmInput"
            placeholder="Describe the alarm in natural language..."
            rows="4"
            class="input textarea"
          ></textarea>

          <div class="form-buttons">
            <button type="button" class="btn-cancel" @click="cancelCreate">Cancel</button>
            <button type="submit" class="btn-create" :disabled="state.loading">
              {{ state.loading ? 'Creating...' : 'Create Alarm' }}
            </button>
          </div>

          <p v-if="state.successMessage" class="text-success">{{ state.successMessage }}</p>
          <p v-if="state.errorMessage" class="text-error">{{ state.errorMessage }}</p>
        </form>
      </div>
    </div>

    <!-- Modal to confirm new alarm creation -->
    <div v-if="state.showNewAlarmModal" class="modal" @click.self="state.showNewAlarmModal = false">
      <div class="modal-content">
        <h3>New Alarm</h3>
        <p>How would you like to create the new alarm?</p>
        <div class="modal-actions">
          <button @click="startNaturalLanguageCreate">Natural Language Description</button>
          <button @click="startManualCreate">Create Manually</button>
          <button @click="state.showNewAlarmModal = false" class="btn-cancel-modal">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 84vh;
}

.sidebar {
  width: 280px;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
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

.new-alarm-btn {
  width: 100%;
  padding: 0.5rem;
  background: #c73659;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.alarm-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.alarm-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.alarm-item:hover {
  background: #f5f5f5;
}

.alarm-item.active {
  background: #e3f2fd;
  border-left: 3px solid #c73659;
}

.alarm-item-title {
  font-weight: bold;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.alarm-item-subtitle {
  font-size: 0.8rem;
  color: #666;
}

.main-area {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background-color: #fff;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.empty-content {
  text-align: center;
  color: #666;
}

.empty-content i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.alarm-form {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.05);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

.input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-save {
  padding: 0.75rem 1.5rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-save:hover {
  background-color: #218838;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  background-color: #5a6268;
}

.btn-create {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-create:hover {
  background-color: #0069d9;
}

.btn-delete {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete:hover {
  background-color: #c82333;
}

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

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.modal-actions button:first-child {
  background: #007bff;
  color: white;
}

.modal-actions button:nth-child(2) {
  background: #28a745;
  color: white;
}

.btn-cancel-modal {
  background: #f8f9fa !important;
  color: #212529 !important;
  border: 1px solid #ddd !important;
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

.empty-list {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.text-success {
  color: #28a745;
  margin-top: 0.5rem;
}

.text-error {
  color: #dc3545;
  margin-top: 0.5rem;
}
</style>
