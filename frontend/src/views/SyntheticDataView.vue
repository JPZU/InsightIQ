<template>
  <body>
    <div class="container">
      <div class="form">
        <div class="form-group">
          <h1 class="text-xl text-center">{{ $t('synthetic_data.title') }}</h1>
          <label class="label">{{ $t('synthetic_data.select_table') }}</label>
          <select v-model="tableName" class="input" :disabled="tables.length === 0">
            <option v-if="tables.length === 0" disabled>{{ $t('synthetic_data.loading_tables') }}</option>
            <option v-for="table in tables" :key="table" :value="table">{{ table }}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="label">{{ $t('synthetic_data.records') }}</label>
          <input v-model.number="numRecords" type="number" class="input small-input" min="1" />
        </div>

        <div class="form-group">
          <label class="label">{{ $t('synthetic_data.details') }}</label>
          <p class="helper-text">
            {{ $t('synthetic_data.details_desc') }}
          </p>
          <p class="helper-text">{{ $t('synthetic_data.request_limit') }}</p>
          <textarea
            v-model="details"
            class="input textarea"
            rows="4"
            maxlength="500"
            :placeholder="$t('synthetic_data.request_example')"
          ></textarea>
        </div>

        <button type="submit" @click="generateData" class="btn" :disabled="loading">
          {{ loading ? $t('synthetic_data.generating') : $t('synthetic_data.generate') }}
        </button>

        <div v-if="response && response.synthetic_data && response.synthetic_data.length">
          <div class="response-box">
            <h2 class="response-title">{{ $t('synthetic_data.generated') }} {{ response.table }}</h2>
            <div v-if="parsedSyntheticData.length > 0">
              <table class="table">
                <thead>
                  <tr>
                    <th v-for="column in tableSchema" :key="column.column_name">
                      {{ column.column_name }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in response.synthetic_data" :key="rowIndex">
                    <td v-for="column in tableSchema" :key="column.column_name">
                      {{ row[column.column_name] || '' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <button class="btn add-btn" @click="addSyntheticDatabase">
              {{ $t('synthetic_data.add_to') }}"{{ tableName }}"
            </button>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      details: '',
      tableName: '',
      numRecords: 10,
      response: null,
      tables: [],
      tableSchema: [],
      loading: false,
    }
  },
  async mounted() {
    await this.fetchTables()
  },
  computed: {
    parsedSyntheticData() {
      if (!this.response || !this.response.synthetic_data) return []

      const rawData = this.response.synthetic_data
      if (rawData.length === 0) return []

      const headers = rawData[0].null

      const rows = rawData.slice(1).map((item) => item.null)

      return [headers, ...rows]
    },
  },
  methods: {
    async fetchTables() {
      try {
        const { data } = await axios.get('http://localhost:8000/api/synthetic_data/tables/')
        this.tables = data.tables
      } catch (error) {
        console.error( $t('synthetic_data.error_tables'), error)
      }
    },
    async generateData() {
      if (!this.tableName) {
        alert($t('synthetic_data.select_table_desc'))
        return
      }
      if (!this.numRecords) {
        alert($t('synthetic_data.select_records'))
        return
      }
      this.loading = true
      this.response = null
      try {
        const { data } = await axios.post(
          'http://localhost:8000/api/synthetic_data/generate/',
          null,
          {
            params: {
              details: this.details,
              table_name: this.tableName,
              num_records: this.numRecords,
            },
          },
        )
        this.response = data
        this.tableSchema = this.response.schema
      } catch (error) {
        console.error($t('synthetic_data.error_data'), error)
        this.response = { error: $t('synthetic_data.error_data_desc') }
      } finally {
        this.loading = false
      }
    },
    addSyntheticDatabase() {
      alert(`Feature not implemented yet, but will add to ${this.tableName}!`)
      console.log($t('synthetic_data.add_to_database'), this.tableName)
    },
  },
}
</script>

<style>
body {
  font-size: 18px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.small-input {
  width: 50%;
}

.center {
  text-align: center;
}

.helper-text {
  font-size: 1rem;
  color: rgb(78, 77, 77);
  margin-bottom: 5px;
}

.btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn:hover {
  background-color: #00356d;
  color: white;
}

.response-box {
  margin-top: 20px;
  overflow-x: auto;
  padding: 10px;
  background: #e9ecef;
  border-radius: 4px;
}

.response-title {
  font-size: 1rem;
  font-weight: bold;
}

.response-content {
  font-size: 0.9rem;
  white-space: pre-wrap;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.table {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
  white-space: nowrap;
}

.add-btn {
  background-color: #28a745;
  margin-top: 10px;
}

.add-btn:hover {
  background-color: #218838;
}
</style>
