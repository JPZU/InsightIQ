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
const chartTitle = ref('')

const submitQuestion = async () => {
  if (!question.value.trim()) return

  loading.value = true
  answer.value = null

  try {
    const response = await ChatService.askQuestion(question.value)
    answer.value = response.response
  } catch (error) {
    console.error(this.$t('chat.error_fetch'), error)
    answer.value = { error: this.$t('chat.error_fetch_desc') }
  } finally {
    loading.value = false
  }
}

const clearFields = () => {
  question.value = ''
  answer.value = null
  chartTitle.value = ''
}

const getButtonClass = (mode) => {
  return viewMode.value === mode ? 'btn-primary text-white' : 'btn-outline-primary'
}

const isValidQueryOutput = (queryOutput) => {
  return queryOutput && !queryOutput.error && Array.isArray(queryOutput) && queryOutput.length > 0
}
</script>

<template>
  <div class="full-page-background">
    <div class="content-container">
      <form class="card" @submit.prevent="submitQuestion">
        <h1 class="text-center mb-3">{{ $t('chat.ask') }}</h1>
        <input
          class="form-control"
          v-model="question"
          :placeholder="$t('chat.type_here')"
          required
        />
        <div class="d-flex gap-2 mt-2">
          <button type="submit" class="btn btn-primary flex-grow-1" :disabled="loading">
            {{ loading ? $t('chat.sending') : $t('chat.send') }}
          </button>
          <button type="button" class="btn btn-secondary" @click="clearFields" :disabled="loading">
            Clear
          </button>
        </div>
      </form>

      <div v-if="answer" class="card mt-3">
        <h3>{{ $t('chat.response') }}</h3>
        <table class="table formatted-table table-bordered">
          <tbody>
            <tr>
              <th scope="row">{{ $t('chat.input') }}</th>
              <td>{{ answer.input || $t('chat.na') }}</td>
            </tr>
            <tr>
              <th scope="row">{{ $t('chat.output') }}</th>
              <td>{{ answer.output || $t('chat.na') }}</td>
            </tr>
            <tr>
              <th scope="row">{{ $t('chat.query') }}</th>
              <td>{{ answer.query || $t('chat.na') }}</td>
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
            v-model="viewMode"
            value="graphs"
          />
          <label :class="`btn ${getButtonClass('graphs')}`" for="viewGraphs">{{
            $t('chat.charts')
          }}</label>

          <input
            type="radio"
            class="btn-check"
            name="viewToggle"
            id="viewTable"
            autocomplete="off"
            v-model="viewMode"
            value="table"
          />
          <label :class="`btn ${getButtonClass('table')}`" for="viewTable">{{
            $t('chat.table')
          }}</label>
        </div>

        <div v-if="viewMode === 'graphs'">
          <div class="mt-3">
            <label for="chart-type">{{ $t('chat.select_chart') }}</label>
            <select id="chart-type" v-model="chartType" class="form-control">
              <option value="bar">{{ $t('chat.bar_chart') }}</option>
              <option value="pie">{{ $t('chat.pie_chart') }}</option>
            </select>
          </div>

          <div class="mt-3">
            <label for="chart-title">Chart Title:</label>
            <input
              id="chart-title"
              v-model="chartTitle"
              class="form-control"
              placeholder="Enter chart title..."
            />
          </div>

          <div
            v-if="!answer.x_axis?.length || !answer.y_axis?.length"
            class="alert alert-info mt-3"
          >
            {{ $t('chat.no_chart') }}
          </div>

          <BarChart
            v-if="chartType === 'bar' && answer.x_axis?.length && answer.y_axis?.length"
            :xAxis="answer.x_axis"
            :yAxis="answer.y_axis"
            :chartTitle="chartTitle || 'Bar Chart'"
          />
          <PieChart
            v-else-if="chartType === 'pie' && answer.x_axis?.length && answer.y_axis?.length"
            :xAxis="answer.x_axis"
            :yAxis="answer.y_axis"
            :chartTitle="chartTitle || 'Pie Chart'"
          />
          <LineChart
            v-else-if="chartType === 'line' && answer.x_axis?.length && answer.y_axis?.length"
            :xAxis="answer.x_axis"
            :yAxis="answer.y_axis"
            :chartTitle="chartTitle || 'Line Chart'"
          />
        </div>

        <div v-else-if="viewMode === 'table'">
          <div v-if="isValidQueryOutput(answer.query_output)">
            <Table :queryOutput="answer.query_output" />
          </div>
          <div v-else class="alert alert-info mt-3">
            {{ $t('chat.no_table') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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

.full-page-background {
  padding: 20px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.content-container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
