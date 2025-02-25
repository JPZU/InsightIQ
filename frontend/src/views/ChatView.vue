<template>
    <div class="container">
        <form class="form-container" @submit.prevent="submitQuestion">
            <h2 class="text-center" style="margin-bottom: 1rem;">Ask your question</h2>
            <div class="mb-3">
                <input class="form-control" id="question" v-model="question" placeholder="Type here..." required
                    style="padding: 10px;">
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? "Sending..." : "Send" }}
            </button>
        </form>

        <!-- Mostrar la respuesta en tabla vertical -->
        <div v-if="answer" class="response-box">
            <h3>Response:</h3>
            <table class="table table-bordered">
                <tbody>
                    <tr>
                        <th scope="row">Input</th>
                        <td>{{ answer.input }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Output</th>
                        <td>{{ answer.output }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Query</th>
                        <td>{{ answer.query }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Query Output</th>
                        <td>{{ answer.query_output }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatService from '@/services/ChatService'

const question = ref('')
const answer = ref(null)
const loading = ref(false)

const submitQuestion = async () => {
    if (!question.value.trim()) return

    loading.value = true
    answer.value = null

    try {
        const response = await ChatService.askQuestion(question.value)
        answer.value = response || { input: "N/A", output: "N/A", query: "N/A", query_output: "N/A" }
    } catch (error) {
        answer.value = { input: "Error", output: "Failed to fetch", query: "-", query_output: "-" }
        console.error(error)
    } finally {
        loading.value = false
        question.value = ''
    }
}
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    max-width: 100%;
    background-color: #f4f4f4;
}

.form-container {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
    text-align: center;
}

.response-box {
    margin-top: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 90%;
    text-align: center;
}

.table {
    margin-top: 1rem;
    width: 100%;
}
</style>
