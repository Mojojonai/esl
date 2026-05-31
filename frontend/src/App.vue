<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
    <AppHeader v-if="authStore.isAuthenticated" />
    <main>
      <RouterView />
    </main>
    <BottomNav v-if="authStore.isAuthenticated && !isAdminRoute" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'
import AppHeader from './components/layout/AppHeader.vue'
import BottomNav from './components/layout/BottomNav.vue'

const router = useRouter()
const authStore = useAuthStore()

const isAdminRoute = computed(() => {
  return router.currentRoute.value.path.includes('/admin')
})

onMounted(() => {
  // Check if user is logged in on app load
  authStore.checkAuthStatus()
})
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}
</style>
