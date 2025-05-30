<template>
  <div class="container">
    <div class="form">
      <h2 class="text-2xl font-bold mb-4 text-center">Edit Alarm</h2>

      <!-- Formulario solo si alarm está lista -->
      <form v-if="alarm" @submit.prevent="updateAlarm" class="space-y-4">
        <div>
          <label class="label">Table Name</label>
          <input v-model="alarm.table_name" class="input" />
        </div>

        <div>
          <label class="label">Field</label>
          <input v-model="alarm.field" class="input" />
        </div>

        <div>
          <label class="label">Condition</label>
          <input v-model="alarm.condition" class="input" />
        </div>

        <div>
          <label class="label">Threshold</label>
          <input v-model="alarm.threshold" class="input" />
        </div>

        <div>
          <label class="label">Description</label>
          <textarea v-model="alarm.description" rows="3" class="input textarea"></textarea>
        </div>

        <div class="checkbox-container">
          <input type="checkbox" id="is_active" v-model="alarm.is_active" class="checkbox" />
          <label for="is_active" class="label ml-2">Active</label>
        </div>

        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save Changes' }}
        </button>
      </form>

      <!-- Mensaje de carga si alarm no está lista -->
      <p v-else class="text-center text-gray-500">Loading alarm...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AlarmService from '@/services/AlarmService'

const route = useRoute()
const router = useRouter()
const loading = ref(false)

// Inicializa alarm como null
const alarm = ref<any>(null)

const fetchAlarm = async () => {
  try {
    const allAlarms = await AlarmService.listAlarms()
    const found = allAlarms.find((a: any) => a.id === Number(route.params.id))
    if (found) {
      alarm.value = {
        ...found,
        is_active: found.is_active === 1, // Convierte 1 a true y 0 a false
      }
    } else {
      console.error('Alarm not found')
    }
  } catch (error) {
    console.error('Error fetching alarm:', error)
  }
}

const updateAlarm = async () => {
  if (!alarm.value) return
  try {
    loading.value = true
    const { id, ...data } = alarm.value
    await AlarmService.updateAlarm(id, data)
    router.push({ name: 'AlarmList' })
  } catch (error) {
    console.error('Error updating alarm:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchAlarm)
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
  padding: 20px;
}

.form {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}

.label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.textarea {
  resize: vertical;
}

.btn {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.btn:hover {
  background-color: #218838;
}

.btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.checkbox-container {
  display: flex;
  align-items: center;
}

.checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
</style>
