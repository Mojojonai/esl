<template>
  <div class="container-main">
    <div class="max-w-md mx-auto mt-16">
      <div class="card">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Change Your Password</h1>
        <p class="text-gray-600 mb-8">This is your first login. Please set a new password.</p>

        <form @submit.prevent="handleChangePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              New Password
            </label>
            <input
              v-model="newPassword"
              type="password"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="Enter new password"
              required
              minlength="6"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <input
              v-model="confirmPassword"
              type="password"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="Confirm password"
              required
              minlength="6"
            />
          </div>

          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="btn-primary w-full"
          >
            <span v-if="isLoading">Changing...</span>
            <span v-else>Change Password</span>
          </button>
        </form>
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

const newPassword = ref('')
const confirmPassword = ref('')
const error = ref('')
const isLoading = ref(false)

const handleChangePassword = async () => {
  error.value = ''

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (newPassword.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  isLoading.value = true
  try {
    await authStore.changePassword('', newPassword.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Failed to change password'
  } finally {
    isLoading.value = false
  }
}
</script>
