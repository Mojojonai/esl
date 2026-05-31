import { defineStore } from 'pinia'
import { ref } from 'vue'
import { learningAPI } from '../services/api'

export const useExerciseStore = defineStore('exercise', () => {
  const levels = ref([])
  const currentLevel = ref(null)
  const units = ref([])
  const currentUnit = ref(null)
  const lessons = ref([])
  const currentLesson = ref(null)
  const exercises = ref([])
  const currentExercise = ref(null)
  const vocabulary = ref([])
  const dialogues = ref([])
  const games = ref([])
  const currentGame = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const fetchLevels = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await learningAPI.getLevels()
      levels.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch levels. Please log in again or check your network connection.'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchUnits = async (levelCode) => {
    isLoading.value = true
    try {
      const response = await learningAPI.getUnits(levelCode)
      units.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch units'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchLessons = async (unitId) => {
    isLoading.value = true
    try {
      const response = await learningAPI.getLessons(unitId)
      lessons.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch lessons'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchExercises = async (lessonId, skillCode = null) => {
    isLoading.value = true
    try {
      const response = await learningAPI.getExercises(lessonId, skillCode)
      exercises.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch exercises'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchExerciseDetail = async (exerciseId) => {
    try {
      const response = await learningAPI.getExerciseDetail(exerciseId)
      currentExercise.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch exercise'
      console.error(err)
    }
  }

  const fetchVocabulary = async (lessonId) => {
    try {
      const response = await learningAPI.getVocabulary(lessonId)
      vocabulary.value = response.data
    } catch (err) {
      console.error('Failed to fetch vocabulary:', err)
    }
  }

  const fetchDialogues = async (lessonId) => {
    try {
      const response = await learningAPI.getDialogues(lessonId)
      dialogues.value = response.data
    } catch (err) {
      console.error('Failed to fetch dialogues:', err)
    }
  }

  const fetchGames = async (lessonId) => {
    try {
      const response = await learningAPI.getGames(lessonId)
      games.value = response.data
    } catch (err) {
      console.error('Failed to fetch games:', err)
    }
  }

  const fetchGameDetail = async (gameId) => {
    try {
      const response = await learningAPI.getGameDetail(gameId)
      currentGame.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch game details'
      console.error(err)
    }
  }

  const submitExercise = async (exerciseId, answer, timeSpent) => {
    try {
      const response = await learningAPI.submitExercise(exerciseId, answer, timeSpent)
      return response.data
    } catch (err) {
      error.value = 'Failed to submit exercise'
      console.error(err)
      throw err
    }
  }

  const submitGame = async (gameId, score, timeSpent) => {
    try {
      const response = await learningAPI.submitGame(gameId, score, timeSpent)
      return response.data
    } catch (err) {
      console.error('Failed to submit game:', err)
      throw err
    }
  }

  const reset = () => {
    levels.value = []
    currentLevel.value = null
    units.value = []
    currentUnit.value = null
    lessons.value = []
    currentLesson.value = null
    exercises.value = []
    currentExercise.value = null
    vocabulary.value = []
    dialogues.value = []
  }

  return {
    levels,
    currentLevel,
    units,
    currentUnit,
    lessons,
    currentLesson,
    exercises,
    currentExercise,
    vocabulary,
    dialogues,
    games,
    isLoading,
    error,
    fetchLevels,
    fetchUnits,
    fetchLessons,
    fetchExercises,
    fetchExerciseDetail,
    fetchVocabulary,
    fetchDialogues,
    fetchGames,
    submitExercise,
    submitGame,
    fetchGameDetail,
    reset,
  }
})
