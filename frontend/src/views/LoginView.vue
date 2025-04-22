<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthService from '@/services/AuthService';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);
const router = useRouter();

async function handleLogin() {
    if (isLoading.value) return;

    errorMessage.value = '';
    isLoading.value = true;

    try {
        const success = await AuthService.login(username.value, password.value);

        if (success) {
            // Redirect to home or dashboard
            router.push('/dashboard');
        } else {
            errorMessage.value = 'Login failed. Please check your credentials.';
        }
    } catch (error) {
        errorMessage.value = error instanceof Error
            ? error.message
            : 'An unexpected error occurred.';
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <div class="login-container">
        <form @submit.prevent="handleLogin" class="login-form">
            <h2>Login</h2>

            <div class="form-group">
                <label for="username">Username or Email</label>
                <input type="text" id="username" v-model="username" required autocomplete="username" />
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" required autocomplete="current-password" />
            </div>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Logging in...' : 'Login' }}
            </button>
        </form>
    </div>
</template>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 1rem;
}

.login-form {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: white;
}

h2 {
    margin-bottom: 1.5rem;
    text-align: center;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

button {
    width: 100%;
    padding: 0.75rem;
    margin-top: 1rem;
    border: none;
    border-radius: 4px;
    background-color: #4f46e5;
    color: white;
    font-size: 1rem;
    cursor: pointer;
}

button:disabled {
    background-color: #a5a5a5;
    cursor: not-allowed;
}

.error-message {
    color: #dc2626;
    margin-top: 0.5rem;
    font-size: 0.875rem;
}
</style>