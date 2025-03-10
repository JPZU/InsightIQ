<template>
    <div class="container">
        <div class="card">
            <h1 class="text-center">File Manager</h1>
            <p class="text-center">Upload CSV or Excel files to load data into the database.</p>

            <div class="upload-section">
                <label class="file-input-container">
                    <input type="file" @change="onFileSelected" accept=".csv,.xls,.xlsx" />
                </label>
                <input type="text" v-model="tableName" placeholder="Table Name" />
                <button @click="uploadFile">Upload File</button>
            </div>

            <p v-if="message" class="message">{{ message }}</p>
        </div>
    </div>
</template>

<script>
import FileManagerService from '@/services/FileManagerService';

export default {
    data() {
        return {
            selectedFile: null,
            tableName: "",
            message: ""
        };
    },
    methods: {
        onFileSelected(event) {
            this.selectedFile = event.target.files[0];
        },
        async uploadFile() {
            if (!this.selectedFile) {
                this.message = "Please select a file.";
                return;
            }
            if (!this.tableName) {
                this.message = "Please enter a table name.";
                return;
            }

            try {
                let response;
                console.log("Uploading file with table name:", this.tableName);
                if (this.selectedFile.name.endsWith(".xls") || this.selectedFile.name.endsWith(".xlsx")) {
                    response = await FileManagerService.uploadExcel(this.selectedFile, this.tableName);
                } else {
                    response = await FileManagerService.uploadCSV(this.selectedFile, this.tableName);
                }
                this.message = response.data.info;
            } catch (error) {
                console.error("Error uploading file:", error);
                this.message = "Error uploading file.";
            }
        }
    }
};
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    text-align: center;
}

.upload-section {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.file-input-container {
    width: 100%;
}

input[type="file"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

input, button {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 8px;
}

button {
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    background-color: #0056b3;
}

.message {
    margin-top: 10px;
    font-weight: bold;
}
</style>
