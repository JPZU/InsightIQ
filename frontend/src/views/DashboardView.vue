<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <section class="file-schema">
      <h2>📄 File Schema: {{ schema.file_name }}</h2>
      <div class="table-wrapper">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Column Name</th>
              <th>Data Type</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="col in schema.columns" :key="col.name">
              <td>{{ col.name }}</td>
              <td>{{ col.type }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>Descriptive Statistics</h2>
      <div class="charts-grid">
        <div
          v-for="(stats, column) in analysis.descriptive_statistics"
          :key="column"
          class="chart-wrapper"
        >
          <h3>{{ column }}</h3>
          <p>There are {{ stats.count }} values in this column.</p>
          <p><strong>Standard Deviation:</strong> {{ stats.std.toFixed(2) }}</p>
          <BarChartDashboard :columnName="column" :stats="filterStats(stats)" />
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import DashboardService from '../services/DashboardService'
import BarChartDashboard from '../components/dashboard/BarChartDashboard.vue'

interface Column {
  name: string
  type: string
}

interface SchemaResponse {
  file_name: string
  columns: Column[]
}

interface AnalysisResponse {
  descriptive_statistics: Record<string, Record<string, number>>
}

const schema = ref<SchemaResponse>({ file_name: '', columns: [] })
const analysis = ref<AnalysisResponse>({ descriptive_statistics: {} })

const fetchDashboardData = async () => {
  try {
    const schemaResponse = await DashboardService.getSchema()
    schema.value = schemaResponse.data

    const analysisResponse = await DashboardService.getAnalysis()
    analysis.value = analysisResponse.data
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
}

const filterStats = (stats: Record<string, number>) => {
  const { std, count, ...filteredStats } = stats
  return filteredStats
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-wrapper {
  background: #f9f9f9;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

.file-schema {
  margin-bottom: 30px;
  background: #fdfdfd;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.file-schema h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  background: white;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  background-color: white;
  border: 1px solid #ddd;
}

.styled-table thead {
  background-color: #f4f4f4;
}

.styled-table th {
  padding: 12px;
  text-align: left;
  font-weight: bold;
  color: #2c3e50;
  border-bottom: 2px solid #ddd;
}

.styled-table td {
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #f1f1f1;
  transition: background-color 0.3s ease;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
