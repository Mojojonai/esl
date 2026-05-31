<template>
  <div class="container-main">
    <!-- Welcome Section -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">
        Welcome, {{ firstName }}! 👋
      </h1>
      <p class="text-gray-600">Ready to learn English today?</p>
    </div>

    <!-- Stats Row -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Level</p>
            <p class="text-2xl font-bold text-blue-600">{{ currentLevel }}</p>
          </div>
          <div class="text-4xl">📚</div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">XP</p>
            <p class="text-2xl font-bold text-green-600">{{ userXP }}</p>
          </div>
          <div class="text-4xl">⭐</div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Streak</p>
            <p class="text-2xl font-bold text-orange-600">{{ userStreak }}</p>
          </div>
          <div class="text-4xl">🔥</div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm">Badges</p>
            <p class="text-2xl font-bold text-purple-600">{{ totalBadges }}</p>
          </div>
          <div class="text-4xl">🏆</div>
        </div>
      </div>
    </div>

    <!-- Main Actions -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <router-link to="/levels" class="card hover:shadow-2xl hover:scale-105 cursor-pointer">
        <div class="text-5xl mb-4">🎓</div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Start Learning</h3>
        <p class="text-gray-600">Continue with lessons</p>
      </router-link>

      <router-link to="/progress" class="card hover:shadow-2xl hover:scale-105 cursor-pointer">
        <div class="text-5xl mb-4">📊</div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">My Progress</h3>
        <p class="text-gray-600">View your statistics</p>
      </router-link>

      <router-link v-if="reviewCount > 0" to="/review" class="card bg-yellow-50 hover:shadow-2xl hover:scale-105 cursor-pointer">
        <div class="text-5xl mb-4">🔄</div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Review {{ reviewCount }}</h3>
        <p class="text-gray-600">Practice weak areas</p>
      </router-link>
    </div>

    <!-- Quick Links -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card">
        <h4 class="font-bold text-gray-900 mb-3">Skills to Practice</h4>
        <div class="space-y-2">
          <div class="flex items-center text-sm text-gray-600">
            <span class="mr-2">👂</span> Listening
          </div>
          <div class="flex items-center text-sm text-gray-600">
            <span class="mr-2">📖</span> Reading
          </div>
          <div class="flex items-center text-sm text-gray-600">
            <span class="mr-2">✍️</span> Writing
          </div>
        </div>
      </div>

      <div class="card">
        <h4 class="font-bold text-gray-900 mb-3">Recent Badges</h4>
        <div v-if="recentBadges.length > 0" class="space-y-2">
          <div v-for="badge in recentBadges.slice(0, 3)" :key="badge.id" class="text-sm text-gray-600">
            🏅 {{ badge.badge.name }}
          </div>
        </div>
        <div v-else class="text-sm text-gray-500">No badges yet. Keep learning!</div>
      </div>

      <div class="card">
        <h4 class="font-bold text-gray-900 mb-3">Tips</h4>
        <ul class="text-sm text-gray-600 space-y-1">
          <li>✓ Practice daily for best results</li>
          <li>✓ Review weak areas regularly</li>
          <li>✓ Earn badges and streaks</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useProgressStore } from '../stores/progressStore'

const authStore = useAuthStore()
const progressStore = useProgressStore()

const currentLevel = ref('A1')
const userXP = ref(0)
const userStreak = ref(0)
const totalBadges = ref(0)
const recentBadges = ref([])
const reviewCount = ref(0)

const firstName = ref(authStore.user?.first_name || 'Learner')

onMounted(async () => {
  // Fetch badges
  await progressStore.fetchBadges()
  recentBadges.value = progressStore.userBadges
  totalBadges.value = progressStore.userBadges.length

  // Fetch review items
  await progressStore.fetchReviewItems()
  reviewCount.value = progressStore.reviewItems.length

  // Simulated user data (from profile)
  userXP.value = authStore.user?.profile?.xp || 0
  userStreak.value = authStore.user?.profile?.streak || 0
  currentLevel.value = authStore.user?.profile?.current_level || 'A1'
})
</script>
