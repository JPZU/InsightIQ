<script setup>
import { computed, ref } from 'vue'
import * as XLSX from 'xlsx'

const props = defineProps({
  queryResult: {
    type: Object,
    required: true,
  },
})

const headers = computed(() => Object.keys(props.queryResult))

const rows = computed(() => {
  const keys = headers.value
  const length = props.queryResult[keys[0]]?.length || 0
  return Array.from({ length }, (_, i) => keys.map((key) => props.queryResult[key][i]))
})

// Paginación
const currentPage = ref(1)
const rowsPerPage = 5

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage
  return rows.value.slice(start, start + rowsPerPage)
})

const totalPages = computed(() => Math.ceil(rows.value.length / rowsPerPage))

// Formato de exportación
const exportFormat = ref('csv') // 'csv' or 'xlsx'

// Exportar la tabla en CSV
const exportToCSV = () => {
  const csvRows = [headers.value.join(',')]
  rows.value.forEach((row) => csvRows.push(row.join(',')))
  const csvContent = csvRows.join('\n')
  const encodedUri = encodeURI('data:text/csv;charset=utf-8,' + csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', 'data.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Exportar la tabla en XLSX
const exportToXLSX = () => {
  const data = rows.value.map((row) => {
    const obj = {}
    row.forEach((cell, i) => {
      obj[headers.value[i]] = cell
    })
    return obj
  })
  const worksheet = XLSX.utils.json_to_sheet(data)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Table')
  XLSX.writeFile(workbook, 'data.xlsx')
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

    <div class="text-center my-3">
      <select v-model="exportFormat" class="form-select me-2">
        <option value="csv">CSV</option>
        <option value="xlsx">XLSX</option>
      </select>
      <button
        @click="exportFormat === 'csv' ? exportToCSV() : exportToXLSX()"
        class="btn btn-primary mt-2"
      >
        Download Table
      </button>
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
