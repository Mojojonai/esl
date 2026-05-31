<template>
  <div class="container-main">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Review & Strengthen Memory</h1>
    
    <div v-if="progressStore.isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading review items...</p>
    </div>

    <div v-else-if="progressStore.reviewItems.length > 0" class="max-w-2xl mx-auto">
      <div v-for="(item, index) in progressStore.reviewItems" :key="item.id" class="card mb-4">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-xl font-bold text-gray-900">{{ item.exercise_title }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ item.exercise_type }}</p>
          </div>
          <span class="text-sm px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
            {{ index + 1 }} of {{ progressStore.reviewItems.length }}
          </span>
        </div>

        <div class="flex gap-3">
          <button
            @click="markCorrect(item.id)"
            class="flex-1 btn-primary"
          >
            ✓ Got It Right
          </button>
          <button
            @click="markIncorrect(item.id)"
            class="flex-1 btn-secondary"
          >
            ✗ Need More Practice
          </button>
        </div>
      </div>
    </div>

    <div v-else class="card text-center py-12">
      <div class="text-5xl mb-4">🎉</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">All Caught Up!</h2>
      <p class="text-gray-600">No exercises to review right now.</p>
      <router-link to="/levels" class="btn-primary inline-block mt-6">
        Start New Lesson
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProgressStore } from '../stores/progressStore'

const progressStore = useProgressStore()

onMounted(() => {
  progressStore.fetchReviewItems()
})

const markCorrect = async (reviewId) => {
  await progressStore.markReviewCorrect(reviewId)
}

const markIncorrect = async (reviewId) => {
  await progressStore.markReviewIncorrect(reviewId)
}
</script>
