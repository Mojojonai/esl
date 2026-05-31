<template>
  <div class="container-main">
    <div v-if="isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading game...</p>
    </div>

    <div v-else-if="error" class="max-w-xl mx-auto mt-16 card">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">Unable to load game</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <router-link to="/dashboard" class="btn-primary">Back to Dashboard</router-link>
    </div>

    <div v-else-if="game" class="max-w-5xl mx-auto py-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ game.title }}</h1>
        <p class="text-gray-600 mt-2">{{ game.description }}</p>
      </div>

      <component
        v-if="gameComponent"
        :key="resetKey"
        :is="gameComponent"
        :game="game"
        @complete="handleGameComplete"
      />

      <div v-else class="card p-8 text-center">
        <h2 class="text-2xl font-semibold text-gray-900 mb-3">Game type not available yet</h2>
        <p class="text-gray-600 mb-6">
          This game type is being built. Please check back for more learning games soon.
        </p>
        <button class="btn-primary" @click="returnToLesson">Choose another activity</button>
      </div>

      <div v-if="completionResult" class="card mt-8 p-6 bg-green-50 border border-green-200">
        <h2 class="text-2xl font-bold text-green-800 mb-3">Great job!</h2>
        <p class="text-gray-700 mb-2">Score: <strong>{{ completionResult.score }}%</strong></p>
        <p class="text-gray-700 mb-4">Time spent: <strong>{{ completionResult.timeSpent }} seconds</strong></p>
        <p class="text-gray-700 mb-4">XP earned: <strong>{{ completionResult.xpEarned }}</strong></p>
        <div class="flex gap-3 flex-wrap">
          <button class="btn-primary" @click="returnToLesson">Back to lesson</button>
          <button class="btn-secondary" @click="restartGame">Play again</button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-600">Game not found.</p>
      <router-link to="/dashboard" class="btn-primary">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useExerciseStore } from '../stores/exerciseStore'
import MemoryMatchGame from '../components/games/MemoryMatchGame.vue'
import SentenceRaceGame from '../components/games/SentenceRaceGame.vue'

const route = useRoute()
const router = useRouter()
const exerciseStore = useExerciseStore()

const isLoading = ref(true)
const error = ref(null)
const completionResult = ref(null)
const game = ref(null)
const resetKey = ref(0)

const gameComponent = computed(() => {
  if (!game.value) return null
  const mapping = {
    memory_match: MemoryMatchGame,
    sentence_race: SentenceRaceGame,
  }
  return mapping[game.value.game_type] || null
})

const loadGame = async () => {
  isLoading.value = true
  error.value = null
  completionResult.value = null

  try {
    const gameId = route.params.gameId
    const gameData = await exerciseStore.fetchGameDetail(gameId)
    if (!gameData) {
      error.value = 'Game data not found.'
    } else {
      game.value = gameData
    }
  } catch (err) {
    error.value = 'Unable to load the game. Please try again later.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

const handleGameComplete = async ({ score, timeSpent }) => {
  try {
    const result = await exerciseStore.submitGame(game.value.id, score, timeSpent)
    completionResult.value = {
      score,
      timeSpent,
      xpEarned: result.xp_earned,
    }
  } catch (err) {
    console.error('Game submission failed:', err)
    error.value = 'Error submitting your game result.'
  }
}

const restartGame = () => {
  completionResult.value = null
  resetKey.value += 1
}

const returnToLesson = () => {
  const lessonId = game.value?.lesson
  if (lessonId) {
    router.push(`/lesson/${lessonId}/exercises`)
  } else {
    router.push('/dashboard')
  }
}

onMounted(loadGame)
</script>
