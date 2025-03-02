<template>
  <div class="p-4 max-w-lg mx-auto">
    <h1 class="text-xl font-bold mb-4">Generate Synthetic Data</h1>
    
    <div class="mb-4">
      <label class="block text-sm font-medium">Select Table</label>
      <select v-model="tableName" class="w-full p-2 border rounded">
        <option value="" disabled>Select a table</option>
        <option v-for="table in tables" :key="table" :value="table">{{ table }}</option>
      </select>
    </div>
    
    <div class="mb-4">
      <label class="block text-sm font-medium">Number of Records</label>
      <input v-model.number="numRecords" type="number" class="w-full p-2 border rounded" min="1" />
    </div>
    
    <button @click="generateData" class="px-4 py-2 bg-blue-500 text-black rounded hover:bg-blue-600">
      Generate Data
    </button>
    
    <div v-if="response" class="mt-4 p-4 border rounded">
      <h2 class="text-lg font-semibold">Response:</h2>
      <pre class="whitespace-pre-wrap text-sm">{{ response }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      tableName: "",
      numRecords: 10,
      response: null,
      tables: [],
    };
  },
  async mounted() {
    await this.fetchTables();
  },
  methods: {
    async fetchTables() {
      try {
        const { data } = await axios.get("http://localhost:8000/api/synthetic_data/tables/");
        this.tables = data.tables;
      } catch (error) {
        console.error("Error fetching tables:", error);
      }
    },
    async generateData() {
      if (!this.tableName) {
        alert("Please enter a table name.");
        return;
      }
      try {
        const { data } = await axios.post("http://localhost:8000/api/synthetic_data/generate/", null, {
          params: {
            table_name: this.tableName,
            num_records: this.numRecords,
          },
        });
        this.response = data;
      } catch (error) {
        console.error("Error generating data:", error);
        this.response = { error: "Failed to generate synthetic data." };
      }
    },
  },
};
</script>

<style>
/* Add any needed styles */
</style>
