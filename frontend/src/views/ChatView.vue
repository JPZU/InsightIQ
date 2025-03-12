<script setup>
import { ref } from 'vue'
import ChatService from '@/services/ChatService'
import BarChart from '@/components/BarChart.vue'
import PieChart from '@/components/PieChart.vue'
import LineChart from '@/components/LineChart.vue'
import Table from '@/components/Table.vue'
import '@/assets/main.css'

const question = ref('')
const answer = ref(null)
const loading = ref(false)
const chartType = ref('bar')
const viewMode = ref('graphs')

const submitQuestion = async () => {
  if (!question.value.trim()) return

  loading.value = true

  try {
    const response = await ChatService.askQuestion(question.value)
    answer.value = response.response
  } catch (error) {
    console.error('Error fetching response:', error)
    answer.value = { error: 'Failed to fetch response. Please try again.' }
  } finally {
    loading.value = false
  }
}

const getButtonClass = (mode) => {
  return viewMode.value === mode
    ? 'btn-primary text-white' // Botón seleccionado
    : 'btn-outline-primary' // Botón no seleccionado
}

// Función para verificar si query_output es válido
const isValidQueryOutput = (queryOutput) => {
  return queryOutput && !queryOutput.error && Array.isArray(queryOutput) && queryOutput.length > 0
}
</script>

<template>
  <div class="full-page-background">
    <div class="content-container">
      <form class="card" @submit.prevent="submitQuestion">
        <h1 class="text-center mb-3">Ask your question</h1>
        <input class="form-control" v-model="question" placeholder="Type here..." required />
        <button type="submit" class="btn btn-primary w-100 mt-2" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send' }}
        </button>
      </form>

      <div v-if="answer" class="card mt-3">
        <h3>Response</h3>
        <table class="table formatted-table table-bordered">
          <tbody>
            <tr>
              <th scope="row">Input</th>
              <td>{{ answer.input || 'N/A' }}</td>
            </tr>
            <tr>
              <th scope="row">Output</th>
              <td>{{ answer.output || 'N/A' }}</td>
            </tr>
            <tr>
              <th scope="row">Query</th>
              <td>{{ answer.query || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Botones para alternar entre gráficos y tabla -->
        <div class="btn-group mt-3" role="group">
          <input
            type="radio"
            class="btn-check"
            name="viewToggle"
            id="viewGraphs"
            autocomplete="off"
            v-model="viewMode"
            value="graphs"
          />
          <label :class="`btn ${getButtonClass('graphs')}`" for="viewGraphs"> Charts </label>

          <input
            type="radio"
            class="btn-check"
            name="viewToggle"
            id="viewTable"
            autocomplete="off"
            v-model="viewMode"
            value="table"
          />
          <label :class="`btn ${getButtonClass('table')}`" for="viewTable"> Table </label>
        </div>

        <!-- Mostrar gráficos o tabla según el modo seleccionado -->
        <div v-if="viewMode === 'graphs'">
          <div class="mt-3">
            <label for="chart-type">Select Chart Type:</label>
            <select id="chart-type" v-model="chartType" class="form-control">
              <option value="bar">Bar Chart</option>
              <option value="pie">Pie Chart</option>
            </select>
          </div>

          <!-- Mensaje si no hay datos para gráficos -->
          <div
            v-if="!answer.x_axis?.length || !answer.y_axis?.length"
            class="alert alert-info mt-3"
          >
            Chart not available. No data to display.
          </div>

          <BarChart
            v-if="chartType === 'bar' && answer.x_axis?.length && answer.y_axis?.length"
            :xAxis="answer.x_axis"
            :yAxis="answer.y_axis"
            :chartTitle="'Bar Chart'"
          />
          <PieChart
            v-else-if="chartType === 'pie' && answer.x_axis?.length && answer.y_axis?.length"
            :xAxis="answer.x_axis"
            :yAxis="answer.y_axis"
            :chartTitle="'Pie Chart'"
          />
        </div>

        <!-- Mostrar tabla solo si query_output es válido -->
        <div v-else-if="viewMode === 'table'">
          <div v-if="isValidQueryOutput(answer.query_output)">
            <Table :queryOutput="answer.query_output" />
          </div>
          <div v-else class="alert alert-info mt-3">
            Table not available. No valid data to display.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Espaciado de los botones */
.btn-group {
  margin-bottom: 1rem;
}

/* Mejor contraste entre los estados de selección */
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

.btn-primary.text-white {
  background-color: #0d6efd !important;
  border-color: #0d6efd !important;
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

.formatted-text {
  max-height: 200px;
  overflow-y: auto;
  padding: 5px;
}
</style>
