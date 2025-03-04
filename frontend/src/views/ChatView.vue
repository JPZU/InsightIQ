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

    const response = await ChatService.askQuestion(question.value)
    console.log(response)
    answer.value = response.response

    loading.value = false

}
</script>

<template>
    <div class="full-page-background">
        <div class="content-container">
            <form class="card" @submit.prevent="submitQuestion">
                <h2 class="text-center mb-3">Ask your question</h2>
                <input class="form-control" v-model="question" placeholder="Type here..." required>
                <button type="submit" class="btn btn-primary w-100 mt-2" :disabled="loading">
                    {{ loading ? "Sending..." : "Send" }}
                </button>
            </form>

            <div v-if="answer" class="card mt-3">
                <h3>Response</h3>
                <table class="table table-bordered">
                    <tbody>
                        <tr>
                            <th scope="row">Input</th>
                            <td>{{ answer.input || "N/A" }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Output</th>
                            <td>{{ answer.output || "N/A" }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Query</th>
                            <td>{{ answer.query || "N/A" }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Query Output</th>
                            <td>{{ answer.query_output || "N/A" }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
