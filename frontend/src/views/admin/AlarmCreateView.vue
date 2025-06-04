<template>
  <div class="container">
    <div class="form">
      <h2 class="text-2xl font-bold mb-4 text-center">{{ $t('admin_alarms.create.title') }}</h2>

      <form @submit.prevent="handleCreate" class="space-y-4">
        <label class="label">{{ $t('admin_alarms.create.description_label') }}</label>
        <textarea
          v-model="userInput"
          :placeholder="$t('admin_alarms.create.description_placeholder')"
          rows="4"
          class="input textarea"
        ></textarea>

        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? $t('admin_alarms.create.button.creating') : $t('admin_alarms.create.button.create') }}
        </button>

        <p v-if="successMessage" class="text-green-600">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-red-600">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AlarmService from '@/services/AlarmService'

const { t } = useI18n()
const userInput = ref('')
const successMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleCreate = async () => {
  try {
    loading.value = true
    await AlarmService.createAlarm(userInput.value)
    successMessage.value = t('admin_alarms.create.messages.success')
    errorMessage.value = ''
    userInput.value = ''
  } catch (error) {
    successMessage.value = ''
    errorMessage.value = t('admin_alarms.create.messages.error')
    console.error(error)
  } finally {
    loading.value = false
  }
}
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

.btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
