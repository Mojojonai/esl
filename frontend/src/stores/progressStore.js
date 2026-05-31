import { defineStore } from 'pinia'
import { ref } from 'vue'
import { progressAPI, learningAPI } from '../services/api'

export const useProgressStore = defineStore('progress', () => {
  const userProgress = ref([])
  const userBadges = ref([])
  const reviewItems = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchProgress = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await progressAPI.getProgress()
      userProgress.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch progress'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchBadges = async () => {
    try {
      const response = await progressAPI.getBadges()
      userBadges.value = response.data
    } catch (err) {
      console.error('Failed to fetch badges:', err)
    }
  }

  const checkAchievements = async () => {
    try {
      const response = await progressAPI.checkAchievements()
      userBadges.value = response.data.all_badges
      return response.data.newly_awarded
    } catch (err) {
      console.error('Failed to check achievements:', err)
    }
  }

  const fetchReviewItems = async () => {
    try {
      const response = await progressAPI.getReviewItems()
      reviewItems.value = response.data
    } catch (err) {
      console.error('Failed to fetch review items:', err)
    }
  }

  const markReviewCorrect = async (reviewId) => {
    try {
      await progressAPI.markReviewCorrect(reviewId)
      await fetchReviewItems()
    } catch (err) {
      console.error('Failed to mark review:', err)
    }
  }

  const markReviewIncorrect = async (reviewId) => {
    try {
      await progressAPI.markReviewIncorrect(reviewId)
      await fetchReviewItems()
    } catch (err) {
      console.error('Failed to mark review:', err)
    }
  }

  const reset = () => {
    userProgress.value = []
    userBadges.value = []
    reviewItems.value = []
  }

  return {
    userProgress,
    userBadges,
    reviewItems,
    isLoading,
    error,
    fetchProgress,
    fetchBadges,
    checkAchievements,
    fetchReviewItems,
    markReviewCorrect,
    markReviewIncorrect,
    reset,
  }
})
