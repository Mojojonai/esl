<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden">
    <div class="grid grid-cols-5 gap-1">
      <router-link
        to="/dashboard"
        class="flex flex-col items-center justify-center py-3 px-2 text-center transition-colors"
        :class="isActive('/dashboard') ? 'text-blue-600 bg-blue-50' : 'text-gray-600'"
      >
        <span class="text-xl">🏠</span>
        <span class="text-xs mt-1">Home</span>
      </router-link>

      <router-link
        to="/levels"
        class="flex flex-col items-center justify-center py-3 px-2 text-center transition-colors"
        :class="isActive('/levels') ? 'text-blue-600 bg-blue-50' : 'text-gray-600'"
      >
        <span class="text-xl">🎓</span>
        <span class="text-xs mt-1">Learn</span>
      </router-link>

      <router-link
        to="/progress"
        class="flex flex-col items-center justify-center py-3 px-2 text-center transition-colors"
        :class="isActive('/progress') ? 'text-blue-600 bg-blue-50' : 'text-gray-600'"
      >
        <span class="text-xl">📊</span>
        <span class="text-xs mt-1">Progress</span>
      </router-link>

      <router-link
        to="/review"
        class="flex flex-col items-center justify-center py-3 px-2 text-center transition-colors"
        :class="isActive('/review') ? 'text-blue-600 bg-blue-50' : 'text-gray-600'"
      >
        <span class="text-xl">🔄</span>
        <span class="text-xs mt-1">Review</span>
      </router-link>

      <button
        @click="showMenu = !showMenu"
        class="flex flex-col items-center justify-center py-3 px-2 text-gray-600 hover:text-gray-900"
      >
        <span class="text-xl">⋮</span>
        <span class="text-xs mt-1">More</span>
      </button>
    </div>
  </nav>

  <!-- Add padding to prevent content overlap on mobile -->
  <div class="h-20 md:h-0"></div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showMenu = ref(false)

const isActive = (path) => {
  return route.path.startsWith(path)
}
</script>
