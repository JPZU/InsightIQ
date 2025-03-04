<script setup>
import { ref } from 'vue'
import ChatService from '@/services/ChatService'
import '@/assets/main.css'

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

<template>
    <div class="full-page-background">
        <div class="content-container">
            <form class="card" @submit.prevent="submitQuestion">
                <h2 class="text-center" style="margin-bottom: 1rem;">Ask your question</h2>
                <div>
                    <input class="form-control" id="question" v-model="question" placeholder="Type here..." required>
                </div>
                <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                    {{ loading ? "Sending..." : "Send" }}
                </button>
            </form>

            <div v-if="answer" class="card mt-3">
                <h3>Response</h3>
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
    </div>
</template>

<style scoped></style>
