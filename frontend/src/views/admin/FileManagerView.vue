<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import FileManagerService from '@/services/FileManagerService'
import { useI18n } from 'vue-i18n'
import axios from '@/axios'

const router = useRouter()
const { t } = useI18n()

const state = reactive({
  selectedFile: null,
  tableName: '',
  message: '',
  tables: [],
  currentTable: null,
  tableInfo: null,
  showDeleteConfirmation: false,
  tableToDelete: '',
  loading: false,
  showNewTableModal: false,
  searchQuery: '',
  loadingTables: false,
  showFileUpload: false,
  uploadType: '', // 'excel' or 'csv'
  showUpdateModal: false,
  replaceData: false,
  showSyntheticDataModal: false, // New state for synthetic data modal
  showGoogleSheetsModal: false, // New state for Google Sheets modal
  googleSheetsUrl: '',
  googleSheetsTableName: '',
})

// Synthetic data state
const syntheticData = reactive({
  numRecords: 10,
  details: '',
  response: null,
  loading: false,
  tableSchema: [],
})

const filteredTables = computed(() => {
  if (!state.searchQuery) return state.tables
  return state.tables.filter((table) =>
    table.toLowerCase().includes(state.searchQuery.toLowerCase()),
  )
})

const onFileSelected = (event) => {
  state.selectedFile = event.target.files[0]
}

const uploadFile = async () => {
  if (!state.selectedFile) {
    state.message = t('file_manager.select_file')
    return
  }
  if (!state.tableName) {
    state.message = t('file_manager.table_name_required')
    return
  }

  state.loading = true
  state.message = ''

  try {
    let response
    if (state.uploadType === 'excel') {
      response = await FileManagerService.uploadExcel(state.selectedFile, state.tableName)
    } else {
      response = await FileManagerService.uploadCSV(state.selectedFile, state.tableName)
    }

    state.message = t('file_manager.upload_success')
    await fetchTables()
    state.showFileUpload = false
    state.selectedFile = null
    state.tableName = ''
  } catch (error) {
    console.error(t('file_manager.error_uploading'), error)
    state.message = t('file_manager.error_uploading')
  } finally {
    state.loading = false
  }
}

const openGoogleSheetsModal = () => {
  state.showGoogleSheetsModal = true
  state.googleSheetsUrl = ''
  state.googleSheetsTableName = ''
}

const closeGoogleSheetsModal = () => {
  state.showGoogleSheetsModal = false
}

const uploadGoogleSheet = async () => {
  if (!state.googleSheetsUrl || !state.googleSheetsTableName) {
    state.message = t('file_manager.url_and_name_required')
    return
  }

  state.loading = true
  state.message = ''

  try {
    await FileManagerService.uploadGoogleSheets(
      state.googleSheetsUrl,
      state.googleSheetsTableName
    )
    
    state.message = t('file_manager.google_sheet_upload_success')
    await fetchTables()
    state.showGoogleSheetsModal = false
  } catch (error) {
    console.error(t('file_manager.error_uploading_google_sheet'), error)
    state.message = t('file_manager.error_uploading_google_sheet')
  } finally {
    state.loading = false
  }
}


const updateTable = async () => {
  if (!state.selectedFile) {
    state.message = t('file_manager.select_file')
    return
  }

  state.loading = true
  state.message = ''

  try {
    const response = await FileManagerService.updateTable(
      state.currentTable,
      state.selectedFile,
      state.replaceData,
    )

    state.message = t('file_manager.update_success')
    await fetchTableData(state.currentTable)
    state.showUpdateModal = false
    state.selectedFile = null
    state.replaceData = false
  } catch (error) {
    console.error(t('file_manager.error_updating'), error)
    state.message = t('file_manager.error_updating')
  } finally {
    state.loading = false
  }
}

const fetchTables = async () => {
  state.loadingTables = true
  try {
    const response = await FileManagerService.getTables()
    state.tables = response.data || []
  } catch (error) {
    console.error('Error fetching tables:', error)
    state.message = t('file_manager.error_fetching_tables')
  } finally {
    state.loadingTables = false
  }
}

const fetchTableData = async (tableName) => {
  try {
    state.currentTable = tableName
    const response = await FileManagerService.getTableInfo(tableName)
    state.tableInfo = response.data
  } catch (error) {
    console.error('Error fetching table data:', error)
    state.message = t('file_manager.error_fetching_data')
  }
}

const deleteTable = async () => {
  if (!state.tableToDelete) return

  try {
    await FileManagerService.deleteTable(state.tableToDelete)
    state.message = t('file_manager.table_deleted', { table: state.tableToDelete })
    state.tableToDelete = ''
    state.showDeleteConfirmation = false
    if (state.currentTable === state.tableToDelete) {
      state.currentTable = null
      state.tableInfo = null
    }
    await fetchTables()
  } catch (error) {
    console.error('Error deleting table:', error)
    state.message = t('file_manager.error_deleting_table')
  }
}

const formatKey = (key) => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

const startFileUpload = (type) => {
  state.uploadType = type
  state.showNewTableModal = false
  state.showFileUpload = true
}

const cancelFileUpload = () => {
  state.showFileUpload = false
  state.selectedFile = null
  state.tableName = ''
}

const startUpdateTable = () => {
  state.showUpdateModal = true
  state.selectedFile = null
  state.replaceData = false
}

function goToSyntheticData() {
  // Open synthetic data modal instead of navigating
  state.showSyntheticDataModal = true
  // Pre-fill with current table name
  syntheticData.tableName = state.currentTable
}

// New synthetic data methods
const generateSyntheticData = async () => {
  if (!syntheticData.numRecords) {
    state.message = t('synthetic_data.select_records')
    return
  }
  syntheticData.loading = true
  syntheticData.response = null
  try {
    const { data } = await axios.post('http://localhost:8000/api/synthetic_data/generate/', null, {
      params: {
        details: syntheticData.details,
        table_name: state.currentTable,
        num_records: syntheticData.numRecords,
      },
    })
    syntheticData.response = data
    syntheticData.tableSchema = syntheticData.response.schema
  } catch (error) {
    console.error(t('synthetic_data.error_data'), error)
    syntheticData.response = { error: t('synthetic_data.error_data_desc') }
  } finally {
    syntheticData.loading = false
  }
}

const addSyntheticDatabase = async () => {
  try {
    state.loading = true

    // Get the data and schema
    const data = syntheticData.response.synthetic_data
    const schema = syntheticData.tableSchema

    if (!data || !data.length || !schema || !schema.length) {
      throw new Error('No synthetic data available')
    }

    // Extract column names from schema
    const headers = schema.map((col) => col.column_name)

    // Convert data to CSV format
    let csvContent = headers.join(',') + '\n'

    // Add each row to CSV
    data.forEach((row) => {
      const csvRow = headers
        .map((header) => {
          // Handle cases where the value might contain commas or quotes
          let value = row[header] || ''

          // Convert values to strings and handle special cases
          if (value === null || value === undefined) {
            return ''
          } else if (typeof value === 'string') {
            // Escape quotes and wrap in quotes if contains comma or quote
            if (value.includes(',') || value.includes('"')) {
              value = value.replace(/"/g, '""')
              return `"${value}"`
            }
            return value
          } else {
            return String(value)
          }
        })
        .join(',')

      csvContent += csvRow + '\n'
    })

    // Convert CSV string to a file
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const csvFile = new File([blob], `${state.currentTable}_synthetic_data.csv`, {
      type: 'text/csv',
    })

    // Send to the updateTable service with replace=false (append mode)
    await FileManagerService.updateTable(state.currentTable, csvFile, false)

    // Update table data to show the changes
    await fetchTableData(state.currentTable)

    // Close modal and show success message
    state.showSyntheticDataModal = false
    state.message = `${data.length} synthetic records were added to ${state.currentTable}`

    // Show notification with success message
    showSuccessNotification(
      `${data.length} synthetic records were successfully added to ${state.currentTable}`,
    )
  } catch (error) {
    console.error('Error adding synthetic data:', error)
    state.message = `Error adding synthetic data to table: ${error.message || 'Unknown error'}`
  } finally {
    state.loading = false
  }
}

const closeSyntheticDataModal = () => {
  state.showSyntheticDataModal = false
  syntheticData.details = ''
  syntheticData.numRecords = 10
  syntheticData.response = null
}

// Parse synthetic data for display
const parsedSyntheticData = computed(() => {
  if (!syntheticData.response || !syntheticData.response.synthetic_data) return []

  const rawData = syntheticData.response.synthetic_data
  if (rawData.length === 0) return []

  if (Array.isArray(rawData[0]?.null)) {
    const headers = rawData[0].null
    const rows = rawData.slice(1).map((item) => item.null)
    return [headers, ...rows]
  }

  return rawData
})

// Fetch tables on component mount
fetchTables()
</script>

<template>
  <div class="app-container">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-header">
        <input v-model="state.searchQuery" placeholder="Search tables..." class="search-input" />
        <button @click="state.showNewTableModal = true" class="new-alarm-btn">+ New Table</button>
      </div>

      <div class="alarm-list">
        <div v-if="state.loadingTables" class="loading-spinner">
          <div class="spinner"></div>
        </div>
        <div v-else-if="state.tables.length === 0" class="empty-list">No tables found</div>
        <div
          v-for="table in filteredTables"
          :key="table"
          @click="fetchTableData(table)"
          :class="['alarm-item', { active: table === state.currentTable }]"
        >
          <div class="alarm-item-title">{{ table }}</div>
          <button
            @click.stop="
              state.tableToDelete = table,
              state.showDeleteConfirmation = true
            "
            class="delete-btn"
          >
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-area">
      <!-- Empty state when no table is selected -->
      <div v-if="!state.currentTable && !state.showFileUpload" class="empty-state">
        <div class="empty-content">
          <i class="bi bi-table"></i>
          <h3>Select a table or create a new one</h3>
        </div>
      </div>

      <!-- File upload form -->
      <div v-if="state.showFileUpload" class="alarm-form">
        <div class="form-header">
          <h2 class="text-2xl font-bold mb-4">
            Upload {{ state.uploadType === 'excel' ? 'Excel' : 'CSV' }} File
          </h2>
        </div>

        <form @submit.prevent="uploadFile" class="space-y-4">
          <div>
            <label class="label">Table Name</label>
            <input v-model="state.tableName" class="input" placeholder="Enter table name" />
          </div>

          <div>
            <label class="label">Select File</label>
            <input
              type="file"
              @change="onFileSelected"
              :accept="state.uploadType === 'excel' ? '.xls,.xlsx' : '.csv'"
              class="input"
            />
          </div>

          <div class="form-buttons">
            <button type="button" class="btn-cancel" @click="cancelFileUpload">Cancel</button>
            <button type="submit" class="btn-save" :disabled="state.loading">
              {{ state.loading ? 'Uploading...' : 'Upload' }}
            </button>
          </div>

          <p v-if="state.message" class="text-error">{{ state.message }}</p>
        </form>
      </div>

      <!-- Table data display -->
      <div v-if="state.currentTable && !state.showFileUpload" class="table-display">
        <div class="table-header">
          <h2 class="text-2xl font-bold">{{ state.currentTable }}</h2>
          <div class="table-actions">
            <button @click="goToSyntheticData" class="btn-create">+ Add Synthetic Data</button>
            <button @click="startUpdateTable" class="btn-save">Update Data</button>
          </div>
        </div>

        <!-- Table schema info -->
        <div v-if="state.tableInfo?.schema" class="schema-info">
          <h3 class="schema-title">Table Schema</h3>
          <div class="schema-grid">
            <div class="schema-header">Column Name</div>
            <div class="schema-header">Data Type</div>
            <div class="schema-header">Nullable</div>
            <div class="schema-header">Primary Key</div>

            <template v-for="column in state.tableInfo.schema" :key="column.column_name">
              <div class="schema-cell">{{ column.column_name }}</div>
              <div class="schema-cell">{{ column.data_type }}</div>
              <div class="schema-cell">{{ column.nullable ? 'Yes' : 'No' }}</div>
              <div class="schema-cell">{{ column.primary_key ? 'Yes' : 'No' }}</div>
            </template>
          </div>
        </div>

        <!-- Sample data display -->
        <div v-if="state.tableInfo?.sample_data" class="sample-data">
          <h3 class="sample-title">Sample Data (First 5 Rows)</h3>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th v-for="column in state.tableInfo.schema" :key="column.column_name">
                    {{ column.column_name }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(_, rowIndex) in Array(5)" :key="rowIndex">
                  <td v-for="column in state.tableInfo.schema" :key="column.column_name">
                    {{ state.tableInfo.sample_data[column.column_name]?.[rowIndex] || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for new table options -->
    <div v-if="state.showNewTableModal" class="modal" @click.self="state.showNewTableModal = false">
      <div class="modal-content">
        <h3>New Table</h3>
        <p>How would you like to create the table?</p>
        <div class="modal-actions">
          <button @click="startFileUpload('excel')">From Excel</button>
          <button @click="startFileUpload('csv')">From CSV</button>
          <button @click="openGoogleSheetsModal">From Google Sheet</button>
          <button @click="state.showNewTableModal = false" class="btn-cancel-modal">Cancel</button>
        </div>
      </div>
    </div>

    <div v-if="state.showGoogleSheetsModal" class="modal" @click.self="closeGoogleSheetsModal">
      <div class="modal-content">
        <h3>Import from Google Sheets</h3>
        <form @submit.prevent="uploadGoogleSheet" class="space-y-4">
          <div>
            <label class="label">Table Name</label>
            <input 
              v-model="state.googleSheetsTableName" 
              class="input" 
              placeholder="Enter table name" 
              required
            />
          </div>

          <div>
            <label class="label">Google Sheet URL</label>
            <input
              v-model="state.googleSheetsUrl"
              class="input"
              placeholder="https://docs.google.com/spreadsheets/d/..."
              required
            />
            <p class="helper-text">
              Make sure the sheet is publicly accessible or shared with your service account
            </p>
          </div>

          <div class="form-buttons">
            <button type="button" class="btn-cancel" @click="closeGoogleSheetsModal">
              Cancel
            </button>
            <button type="submit" class="btn-save" :disabled="state.loading">
              {{ state.loading ? 'Importing...' : 'Import Sheet' }}
            </button>
          </div>

          <p v-if="state.message" class="text-error">{{ state.message }}</p>
        </form>
      </div>
    </div>

    <!-- Modal for updating table -->
    <div v-if="state.showUpdateModal" class="modal" @click.self="state.showUpdateModal = false">
      <div class="modal-content">
        <h3>Update Table: {{ state.currentTable }}</h3>
        <form @submit.prevent="updateTable" class="space-y-4">
          <div>
            <label class="label">Select File</label>
            <input type="file" @change="onFileSelected" accept=".csv,.xls,.xlsx" class="input" />
          </div>
          <div class="checkbox-group">
            <input type="checkbox" id="replaceData" v-model="state.replaceData" />
            <label for="replaceData">Replace existing data</label>
          </div>
          <div class="form-buttons">
            <button type="button" class="btn-cancel" @click="state.showUpdateModal = false">
              Cancel
            </button>
            <button type="submit" class="btn-save" :disabled="state.loading || !state.selectedFile">
              {{ state.loading ? 'Updating...' : 'Update' }}
            </button>
          </div>
          <p v-if="state.message" class="text-error">{{ state.message }}</p>
        </form>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <div
      v-if="state.showDeleteConfirmation"
      class="modal"
      @click.self="state.showDeleteConfirmation = false"
    >
      <div class="modal-content">
        <span class="close" @click="state.showDeleteConfirmation = false">&times;</span>
        <h3>Confirm Deletion</h3>
        <p>Are you sure you want to delete "{{ state.tableToDelete }}"?</p>
        <div class="modal-actions">
          <button @click="state.showDeleteConfirmation = false" class="btn-cancel-modal">
            Cancel
          </button>
          <button @click="deleteTable" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>

    <!-- NEW Synthetic Data Modal -->
    <div v-if="state.showSyntheticDataModal" class="modal">
      <div class="modal-content synthetic-modal">
        <span class="close" @click="closeSyntheticDataModal">&times;</span>
        <h3 class="synthetic-title">{{ $t('synthetic_data.title', 'Generate Synthetic Data') }}</h3>

        <div class="form-group">
          <label class="label">{{ $t('synthetic_data.table_name', 'Table') }}</label>
          <div class="selected-table">{{ state.currentTable }}</div>
        </div>

        <div class="form-group">
          <label class="label">{{ $t('synthetic_data.records', 'Number of Records') }}</label>
          <input
            v-model.number="syntheticData.numRecords"
            type="number"
            class="input small-input"
            min="1"
          />
        </div>

        <div class="form-group">
          <label class="label">{{ $t('synthetic_data.details', 'Details') }}</label>
          <p class="helper-text">
            {{ $t('synthetic_data.details_desc', 'Specify requirements for the synthetic data') }}
          </p>
          <p class="helper-text">{{ $t('synthetic_data.request_limit', 'Limit: 500 chars') }}</p>
          <textarea
            v-model="syntheticData.details"
            class="input textarea"
            rows="4"
            maxlength="500"
            :placeholder="
              $t(
                'synthetic_data.request_example',
                'Example: Generate realistic customer data with names, ages between 18-65, and purchases reflecting seasonal trends.',
              )
            "
          ></textarea>
        </div>

        <button @click="generateSyntheticData" class="btn" :disabled="syntheticData.loading">
          {{
            syntheticData.loading
              ? $t('synthetic_data.generating', 'Generating...')
              : $t('synthetic_data.generate', 'Generate Data')
          }}
        </button>

        <!-- Generated Data Display -->
        <div
          v-if="
            syntheticData.response &&
            syntheticData.response.synthetic_data &&
            syntheticData.response.synthetic_data.length
          "
          class="response-box"
        >
          <h2 class="response-title">
            {{ $t('synthetic_data.generated', 'Generated Data for') }} {{ state.currentTable }}
          </h2>

          <div class="table-container">
            <table class="table">
              <thead>
                <tr>
                  <th v-for="column in syntheticData.tableSchema" :key="column.column_name">
                    {{ column.column_name }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, rowIndex) in syntheticData.response.synthetic_data"
                  :key="rowIndex"
                >
                  <td v-for="column in syntheticData.tableSchema" :key="column.column_name">
                    {{ row[column.column_name] || '' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <button class="btn add-btn" @click="addSyntheticDatabase">
            {{ $t('synthetic_data.add_to', 'Add to') }} "{{ state.currentTable }}"
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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
}

.delete-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 1rem;
  padding: 0 5px;
}

.delete-btn:hover {
  color: #c82333;
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

.table-display {
  max-width: 1200px;
  margin: 0 auto;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.table-actions {
  display: flex;
  gap: 1rem;
}

.schema-info {
  margin-bottom: 2rem;
}

.schema-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.schema-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background-color: #ddd;
  border: 1px solid #ddd;
  margin-bottom: 2rem;
}

.schema-header {
  background-color: #f2f2f2;
  padding: 0.75rem;
  font-weight: bold;
}

.schema-cell {
  background-color: white;
  padding: 0.75rem;
}

.sample-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.form-header {
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

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
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

.btn-delete {
  padding: 0.5rem 1rem;
  background-color: #dc3545 !important;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete:hover {
  background-color: #c82333 !important;
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

.modal-actions button:nth-child(3) {
  background: #8e28a7;
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

.text-error {
  color: #dc3545;
  margin-top: 0.5rem;
}

.table-container {
  margin-top: 1rem;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

/* Synthetic Data Modal Styles */
.synthetic-modal {
  width: 800px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.synthetic-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #c73659;
  padding-bottom: 0.75rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.selected-table {
  padding: 0.75rem;
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-weight: 500;
}

.helper-text {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.small-input {
  width: 120px;
}

.textarea {
  min-height: 100px;
  resize: vertical;
}

.btn {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  display: block;
  margin: 0 auto;
  width: fit-content;
}

.btn:hover {
  background-color: #0069d9;
}

.btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.response-box {
  margin-top: 2rem;
  border-top: 1px solid #e0e0e0;
  padding-top: 1.5rem;
}

.response-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.add-btn {
  margin-top: 1.5rem;
  background-color: #28a745;
}

.add-btn:hover {
  background-color: #218838;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  margin-top: -10px;
}

.close:hover {
  color: #333;
}

/* Table styles specific to synthetic data */
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.table th {
  background-color: #f2f2f2;
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
  font-weight: bold;
  position: sticky;
  top: 0;
}

.table td {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.table-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  margin: 1rem 0;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .synthetic-modal {
    width: 95%;
  }

  .table-container {
    max-height: 250px;
  }
}
</style>
