<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  queryResult: {
    type: Object,
    required: true
  }
})

const headers = computed(() => Object.keys(props.queryResult))

const rows = computed(() => {
  const keys = headers.value
  const length = props.queryResult[keys[0]]?.length || 0
  return Array.from({ length }, (_, i) => keys.map(key => props.queryResult[key][i]))
})

// Paginación
const currentPage = ref(1)
const rowsPerPage = 5

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage
  return rows.value.slice(start, start + rowsPerPage)
})

const totalPages = computed(() => Math.ceil(rows.value.length / rowsPerPage))

// Exportar a CSV
const exportToCSV = () => {
  const csvRows = [headers.value.join(',')]
  rows.value.forEach(row => csvRows.push(row.join(',')))
  const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' })
  saveAs(blob, 'data.csv')
}
</script>

<template>
  <div class="table-responsive">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in paginatedRows" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>

    <div class="text-center mb-3">
      <button @click="exportToCSV" class="btn btn-primary">Export to CSV</button>
    </div>

    <!-- Paginación -->
    <div class="pagination-container">
      <button class="btn btn-outline-primary" :disabled="currentPage === 1" @click="currentPage--">
        Previous
      </button>

      <span class="page-indicator"> Page {{ currentPage }} of {{ totalPages }} </span>

      <button
        class="btn btn-outline-primary"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Next
      </button>
    </div>
  </div>
</template>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.page-indicator {
  margin: 0 15px;
  font-weight: bold;
}
</style>
