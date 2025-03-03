<template>
<body>
  <div class="container">
    <h1 class=" text-xl">Generate Synthetic Data</h1>

    <div class="form">
      <div class="form-group">
        <label class="label">Select Table</label>
        <select v-model="tableName" class="input" :disabled="tables.length === 0">
        <option v-if="tables.length === 0" disabled>Loading tables...</option>
        <option v-for="table in tables" :key="table" :value="table">{{ table }}</option>
      </select>

      </div>

      <div class="form-group">
        <label class="label">Number of Records</label>
        <input v-model.number="numRecords" type="number" class="input small-input" min="1" />
      </div>

      <div class="form-group">
        <label class="label">Details</label>
        <p class="helper-text">If you'd like, give us more details about the style the synthetic data should have.</p>
        <textarea v-model="details" class="input textarea" rows="4" maxlength="600" placeholder="e.g.: Make all people older than 35 years old."></textarea>
      </div>

      <button type="submit" @click="generateData" class="btn" :disabled="loading">
        {{ loading ? "Generating..." : "Generate Data" }}
      </button>

      <div v-if="response" class="response-box">
        <h2 class="response-title">Response:</h2>
        <pre class="response-content">{{ response }}</pre>
        
        <button class="btn add-btn" @click="addSyntheticDatabase">
          Add data to "{{ tableName }}"
        </button>
      </div>
    </div>
  </div>
</body>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      details: "",
      tableName: "",
      numRecords: 10,
      response: null,
      tables: [],
      loading: false,
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
        alert("Please select a table.");
        return;
      }
      if (!this.numRecords) {
        alert("Please select an amount of records to generate.");
        return;
      }
      this.loading = true;
      this.response = null;
      try {
        const { data } = await axios.post("http://localhost:8000/api/synthetic_data/generate/", null, {
          params: {
            details: this.details,
            table_name: this.tableName,
            num_records: this.numRecords,
          },
        });
        this.response = data;
      } catch (error) {
        console.error("Error generating data:", error);
        this.response = { error: "Failed to generate synthetic data." };
      } finally {
        this.loading = false;
      }
    },
    addSyntheticDatabase() {
      alert(`Feature not implemented yet, but will add to ${this.tableName}!`);
      console.log("Adding synthetic database to:", this.tableName);
    },
  },
};
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
  max-width: 700px;
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

.add-btn {
  background-color: #28a745; 
  margin-top: 10px;
}

.add-btn:hover {
  background-color: #218838; 
}
</style>
