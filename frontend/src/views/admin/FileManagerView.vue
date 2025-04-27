<template>
  <div class="container">
    <div class="card">
      <h1 class="text-center">{{ $t('file_manager.title') }}</h1>
      <p class="text-center">{{ $t('file_manager.instructions') }}</p>

      <div class="upload-section">
        <label class="file-input-container">
          <input type="file" @change="onFileSelected" accept=".csv,.xls,.xlsx" />
        </label>
        <input type="text" v-model="tableName" :placeholder="$t('file_manager.table_name')" />
        <button @click="uploadFile">{{ $t('file_manager.upload') }}</button>
      </div>

      <p v-if="message" class="message">{{ message }}</p>
      
      <!-- Modal for triggered alarms -->
      <div v-if="triggeredAlarms.length" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <h3>Triggered Alarms</h3>
          <ul>
            <li v-for="(alarm, index) in triggeredAlarms" :key="index">
              <p><strong>The alarm with ID {{ alarm.alarm_id }} was triggered:</strong></p>
              <p><strong>Description:</strong> {{ alarm.description }}</p>
              <p><strong>Triggered Data:</strong></p>
              <ul>
                <li v-for="(value, key) in alarm.triggered_data" :key="key">
                  <strong>{{ formatKey(key) }}:</strong> {{ value || 'N/A' }}
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FileManagerService from '@/services/FileManagerService'

export default {
  data() {
    return {
      selectedFile: null,
      tableName: '',
      message: '',
      triggeredAlarms: [], // To hold triggered alarms
    }
  },
  methods: {
    onFileSelected(event) {
      this.selectedFile = event.target.files[0]
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.message = this.$t('file_manager.select_file')
        return
      }
      if (!this.tableName) {
        this.message = this.$t('file_manager.table_name_required')
        return
      }

      try {
        let response
        console.log(this.$t('file_manager.uploading'), this.tableName)
        if (this.selectedFile.name.endsWith('.xls') || this.selectedFile.name.endsWith('.xlsx')) {
          response = await FileManagerService.uploadExcel(this.selectedFile, this.tableName)
        } else {
          response = await FileManagerService.uploadCSV(this.selectedFile, this.tableName)
        }
        this.message = response.data.info
        this.triggeredAlarms = response.data.triggered_alarms || [] // Set triggered alarms
      } catch (error) {
        console.error(this.$t('file_manager.error_uploading'), error)
        this.message = this.$t('file_manager.error_uploading')
      }
    },
    closeModal() {
      this.triggeredAlarms = [] // Close the modal by clearing the alarms
    },
    formatKey(key) {
      // Function to format keys for better readability
      return key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
    }
  },
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  text-align: center;
}

.upload-section {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.file-input-container {
  width: 100%;
}

input[type='file'] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input,
button {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.message {
  margin-top: 10px;
  font-weight: bold;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  text-align: left;
}

.close {
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
