<template>
  <div class="container-main">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Select Your Level</h1>
    
    <div v-if="exerciseStore.isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading levels...</p>
    </div>

    <div v-else-if="exerciseStore.error" class="max-w-3xl mx-auto p-8 bg-red-50 border border-red-200 rounded-lg text-center">
      <h2 class="text-2xl font-semibold text-red-800 mb-3">Unable to load levels</h2>
      <p class="text-red-700 mb-4">{{ exerciseStore.error }}</p>
      <button @click="exerciseStore.fetchLevels" class="btn-primary">Retry</button>
    </div>

    <div v-else-if="exerciseStore.levels.length === 0" class="text-center py-12">
      <p class="text-gray-600">No learning levels are available right now.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
      <router-link
        v-for="level in exerciseStore.levels"
        :key="level.id"
        :to="`/level/${level.code}/units`"
        class="card hover:shadow-xl cursor-pointer group"
      >
        <div class="text-5xl mb-4 group-hover:scale-125 transition-transform">
          {{ getLevelEmoji(level.code) }}
        </div>
        <h3 class="text-xl font-bold text-gray-900">{{ level.name }}</h3>
        <p class="text-gray-600 text-sm mt-2">{{ level.description }}</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useExerciseStore } from '../stores/exerciseStore'

const exerciseStore = useExerciseStore()

const getLevelEmoji = (code) => {
  const emojis = { 'A1': '🌱', 'A2': '🌿', 'B1': '🌳', 'B2': '🏔️', 'C1': '🌟' }
  return emojis[code] || '📚'
}

onMounted(() => {
  exerciseStore.fetchLevels()
})
</script>
