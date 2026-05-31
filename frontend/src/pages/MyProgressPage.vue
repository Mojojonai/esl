<template>
  <div class="container-main">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">My Progress</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Progress by Skill -->
      <div class="lg:col-span-2">
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Skills Progress</h2>
          <div v-if="progressStore.userProgress.length > 0" class="space-y-4">
            <div v-for="progress in progressStore.userProgress" :key="progress.id" class="border-b pb-4">
              <div class="flex justify-between items-center mb-2">
                <span class="font-semibold text-gray-900">{{ progress.skill_details.name }}</span>
                <span class="text-sm text-gray-600">{{ progress.progress_percent }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${progress.progress_percent}%` }"
                />
              </div>
              <div class="flex justify-between text-xs text-gray-600 mt-1">
                <span>{{ progress.completed_exercises }}/{{ progress.total_exercises }}</span>
                <span>Avg: {{ Math.round(progress.average_score) }}%</span>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-600">No progress yet. Start learning!</div>
        </div>
      </div>

      <!-- Badges -->
      <div>
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Badges</h2>
          <div v-if="progressStore.userBadges.length > 0" class="space-y-3">
            <div v-for="badge in progressStore.userBadges.slice(0, 5)" :key="badge.id" class="text-center">
              <div class="text-3xl mb-1">🏅</div>
              <p class="text-sm font-semibold text-gray-900">{{ badge.badge.name }}</p>
              <p class="text-xs text-gray-600">Earned</p>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-600">
            <p class="text-3xl mb-2">🎯</p>
            <p>No badges yet.</p>
            <p class="text-sm">Keep practicing!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProgressStore } from '../stores/progressStore'

const progressStore = useProgressStore()

onMounted(() => {
  progressStore.fetchProgress()
  progressStore.fetchBadges()
})
</script>
