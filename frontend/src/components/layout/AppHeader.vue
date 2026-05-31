<template>
  <header class="bg-white shadow-md sticky top-0 z-50">
    <div class="container-main max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
      <router-link to="/dashboard" class="flex items-center gap-2">
        <span class="text-2xl">📚</span>
        <span class="text-2xl font-bold text-blue-600">EnglishNow</span>
      </router-link>

      <div class="hidden md:flex items-center gap-6">
        <span class="text-sm text-gray-600">
          Welcome, {{ firstName }}
        </span>
        <button
          @click="handleLogout"
          class="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>

      <button
        @click="showMobileMenu = !showMobileMenu"
        class="md:hidden text-gray-600 hover:text-gray-900"
      >
        ☰
      </button>
    </div>

    <!-- Mobile Menu -->
    <div v-if="showMobileMenu" class="md:hidden bg-gray-50 border-t p-4">
      <div class="flex flex-col gap-4">
        <span class="text-sm text-gray-600">Welcome, {{ firstName }}</span>
        <button
          @click="handleLogout"
          class="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors text-left"
        >
          Logout
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const showMobileMenu = ref(false)
const firstName = computed(() => authStore.user?.first_name || 'Learner')

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
