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

    <!-- Paginación -->
    <div class="pagination-container">
      <button 
        class="btn btn-outline-primary"
        :disabled="currentPage === 1"
        @click="currentPage--"
      >
        Anterior
      </button>

      <span class="page-indicator"> Página {{ currentPage }} de {{ totalPages }} </span>

      <button 
        class="btn btn-outline-primary"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  queryOutput: {
    type: Array,
    required: true,
  },
});

const currentPage = ref(1);
const rowsPerPage = 5; // Máximo de registros por página

// Extraer encabezados de la primera fila si existen
const headers = computed(() => {
  if (props.queryOutput.length > 0 && Array.isArray(props.queryOutput[0])) {
    return props.queryOutput[0].map((_, index) => `Column ${index + 1}`);
  }
  return [];
});

// Cálculo de paginación
const totalPages = computed(() => Math.ceil(props.queryOutput.length / rowsPerPage));

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage;
  return props.queryOutput.slice(start, start + rowsPerPage);
});
</script>

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
