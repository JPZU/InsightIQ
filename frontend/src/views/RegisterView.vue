<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import UserService from '@/services/UserService'
import AuthService from '@/services/AuthService'

const fullName = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const router = useRouter()

async function handleRegister() {
  if (isLoading.value) return

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  try {
    // First, register the user
    const registerResponse = await UserService.register({
      full_name: fullName.value,
      username: username.value,
      email: email.value,
      password: password.value,
    })

    console.log('Registration response:', registerResponse)

    if (registerResponse.success) {
      // If registration is successful, automatically log the user in
      try {
        const loginSuccess = await AuthService.login(username.value, password.value)

        if (loginSuccess) {
          // Before redirecting, ensure we have a short delay for state to update
          setTimeout(() => {
            // Explicitly dispatch an auth state change event
            window.dispatchEvent(
              new CustomEvent('auth-state-changed', {
                detail: { isAuthenticated: true },
              }),
            )

            // Then redirect to home page
            router.push('/')
          }, 100)
        } else {
          // If login fails for some reason, still show registration success but redirect to login
          console.warn('Registration successful but automatic login failed')
          errorMessage.value =
            'Account created successfully, but login failed. Please try logging in manually.'
          setTimeout(() => {
            router.push('/login')
          }, 3000) // Give user time to read the message before redirecting
        }
      } catch (loginError) {
        // Handle login error
        console.error('Auto-login error after registration:', loginError)
        errorMessage.value =
          'Account created successfully, but automatic login failed. Please try logging in manually.'
        setTimeout(() => {
          router.push('/login')
        }, 3000) // Give user time to read the message before redirecting
      }
    } else {
      // Registration failed
      errorMessage.value = registerResponse.message || 'Registration failed. Please try again.'
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'An unexpected error occurred.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="register-container">
    <form @submit.prevent="handleRegister" class="register-form">
      <h2>Create an Account</h2>

      <div class="form-group">
        <label for="fullName">Full Name</label>
        <input type="text" id="fullName" v-model="fullName" required autocomplete="name" />
      </div>

      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required autocomplete="username" />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required autocomplete="email" />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          autocomplete="new-password"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          required
          autocomplete="new-password"
        />
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Creating account...' : 'Register' }}
      </button>

      <div class="login-link">
        Already have an account? <router-link to="/login">Login here</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 1rem;
}

.register-form {
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
  background-color: #43a3e7;
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

.login-link {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
}

.login-link a {
  color: #43a3e7;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
