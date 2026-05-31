<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-3xl shadow-2xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">EnglishNow</h1>
          <p class="text-gray-600">Learn English, Your Way</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              v-model="username"
              type="text"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="Enter your username"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              v-model="password"
              type="password"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="Enter your password"
              required
            />
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">
            {{ error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="authStore.isLoading">Loading...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <!-- Demo Credentials -->
        <div class="mt-8 p-4 bg-blue-50 rounded-lg">
          <p class="text-sm font-medium text-gray-700 mb-2">Demo Credentials:</p>
          <p class="text-xs text-gray-600"><strong>Learner:</strong> learner1 / learner123</p>
          <p class="text-xs text-gray-600"><strong>Admin:</strong> admin / admin123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  try {
    const response = await authStore.login(username.value, password.value)
    if (response.profile?.first_login && response.profile?.password_changed === false) {
      router.push('/first-password-change')
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    error.value = authStore.error || 'Login failed. Please try again.'
  }
}
</script>
