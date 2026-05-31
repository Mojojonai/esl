<template>
  <div class="container-main">
    <div v-if="exerciseStore.isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading exercise...</p>
    </div>

    <div v-else-if="currentExercise" class="max-w-2xl mx-auto">
      <!-- Exercise Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">{{ currentExercise.title }}</h1>
        <p class="text-gray-600 mt-2">{{ currentExercise.instruction }}</p>
      </div>

      <!-- Exercise Component -->
      <ExerciseRenderer
        :exercise="currentExercise"
        @submit="handleSubmit"
        @skip="handleSkip"
      />

      <!-- Linked lesson games -->
      <div v-if="exerciseStore.games.length > 0" class="mt-10">
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Mini-games for this lesson</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <router-link
            v-for="game in exerciseStore.games"
            :key="game.id"
            :to="`/game/${game.id}`"
            class="card hover:shadow-xl transition-shadow"
          >
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-xl font-semibold text-gray-900">{{ game.title }}</h3>
                <p class="text-gray-600 text-sm mt-2">{{ game.description }}</p>
              </div>
              <div class="text-indigo-500 text-3xl">🎮</div>
            </div>
            <div class="mt-3 text-sm text-gray-500">XP reward: {{ game.xp_reward }}</div>
          </router-link>
        </div>
      </div>

      <!-- Feedback (after submission) -->
      <div v-if="feedback" class="mt-8">
        <FeedbackBox :feedback="feedback" @next="handleNext" />
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-600">No exercise found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useExerciseStore } from '../stores/exerciseStore'
import ExerciseRenderer from '../components/exercises/ExerciseRenderer.vue'
import FeedbackBox from '../components/shared/FeedbackBox.vue'

const route = useRoute()
const router = useRouter()
const exerciseStore = useExerciseStore()

const currentExercise = ref(null)
const feedback = ref(null)
const startTime = ref(null)
const currentIndex = ref(0)

const setCurrentExercise = (exercise, index = 0) => {
  currentExercise.value = exercise
  currentIndex.value = index
  feedback.value = null
  startTime.value = Date.now()
}

const loadExercisesForLesson = async (lessonId) => {
  await exerciseStore.fetchExercises(lessonId)
  if (exerciseStore.exercises.length > 0) {
    setCurrentExercise(exerciseStore.exercises[0], 0)
  }
}

const loadExerciseById = async (exerciseId) => {
  const exercise = await exerciseStore.fetchExerciseDetail(exerciseId)
  if (exercise) {
    await exerciseStore.fetchExercises(exercise.lesson)
    await exerciseStore.fetchGames(exercise.lesson)
    const index = exerciseStore.exercises.findIndex((item) => item.id === exercise.id)
    setCurrentExercise(exercise, index >= 0 ? index : 0)
  }
}

onMounted(() => {
  if (route.params.exerciseId) {
    loadExerciseById(route.params.exerciseId)
  } else if (route.params.lessonId) {
    loadExercisesForLesson(route.params.lessonId)
  }

  if (route.params.lessonId) {
    exerciseStore.fetchGames(route.params.lessonId)
  }
})

watch(
  () => route.params.lessonId,
  (lessonId) => {
    if (lessonId) {
      loadExercisesForLesson(lessonId)
    }
  }
)

const handleSubmit = async (answer) => {
  if (!currentExercise.value) return

  const timeSpent = Math.floor((Date.now() - startTime.value) / 1000)
  try {
    const result = await exerciseStore.submitExercise(currentExercise.value.id, answer, timeSpent)
    feedback.value = result
  } catch (err) {
    console.error('Failed to submit exercise:', err)
  }
}

const goToNextExercise = () => {
  if (!exerciseStore.exercises.length) {
    return
  }

  const nextIndex = currentIndex.value + 1
  if (nextIndex < exerciseStore.exercises.length) {
    setCurrentExercise(exerciseStore.exercises[nextIndex], nextIndex)
  } else {
    const lessonId = route.params.lessonId || currentExercise.value?.lesson
    if (lessonId) {
      router.push(`/lesson/${lessonId}/exercises`)
    } else {
      router.push('/levels')
    }
  }
}

const handleSkip = () => {
  feedback.value = null
  goToNextExercise()
}

const handleNext = () => {
  feedback.value = null
  goToNextExercise()
}
</script>
