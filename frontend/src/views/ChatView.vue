<script setup>
import { ref } from 'vue'
import ChatService from '@/services/ChatService'
import BarChart from '@/components/BarChart.vue'
import PieChart from '@/components/PieChart.vue'
import LineChart from '@/components/LineChart.vue'
import '@/assets/main.css'

const question = ref('')
const answer = ref(null)
const loading = ref(false)
const chartType = ref('bar')

const submitQuestion = async () => {
  if (!question.value.trim()) return

  loading.value = true

  const response = await ChatService.askQuestion(question.value)
  answer.value = response.response

  loading.value = false
}
</script>

<template>
  <div class="full-page-background">
    <div class="content-container">
      <form class="card" @submit.prevent="submitQuestion">
        <h2 class="text-center mb-3">Ask your question</h2>
        <input class="form-control" v-model="question" placeholder="Type here..." required />
        <button type="submit" class="btn btn-primary w-100 mt-2" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send' }}
        </button>
      </form>

      <div v-if="answer" class="card mt-3">
        <h3>Response</h3>
        <table class="table table-bordered">
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
            <tr>
              <th scope="row">Query Output</th>
              <td>{{ answer.query_output || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>

         <!-- Selector de tipo de gráfico -->
         <div class="mt-3">
          <label for="chart-type">Select Chart Type:</label>
          <select id="chart-type" v-model="chartType" class="form-control">
            <option value="bar">Bar Chart</option>
            <option value="pie">Pie Chart</option>
            <option value="line">Line Chart</option>
          </select>
        </div>

        <BarChart
          v-if="chartType === 'bar' && answer.x_axis && answer.x_axis.length >= 1 && answer.y_axis && answer.y_axis.length >= 1"
          :xAxis="answer.x_axis"
          :yAxis="answer.y_axis"
          :chartTitle="'Bar Chart'"
        />
        <PieChart
          v-else-if="chartType === 'pie' && answer.x_axis && answer.x_axis.length >= 1 && answer.y_axis && answer.y_axis.length >= 1"
          :xAxis="answer.x_axis"
          :yAxis="answer.y_axis"
          :chartTitle="'Pie Chart'"
        />
        <LineChart
          v-else-if="chartType === 'line' && answer.x_axis && answer.x_axis.length >= 1 && answer.y_axis && answer.y_axis.length >= 1"
          :xAxis="answer.x_axis"
          :yAxis="answer.y_axis"
          :chartTitle="'Line Chart'"
        />

      </div>
    </div>
  </div>
</template>

<style scoped></style>
