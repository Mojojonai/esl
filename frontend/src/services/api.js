import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Handle responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (username, password) =>
    apiClient.post('auth/login/', { username, password }),
  logout: () =>
    apiClient.post('auth/logout/'),
  changePassword: (oldPassword, newPassword) =>
    apiClient.post('auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPassword,
    }),
  getMe: () =>
    apiClient.get('users/me/'),
}

export const learningAPI = {
  getLevels: () =>
    apiClient.get('levels/'),
  getUnits: (levelCode) =>
    apiClient.get('units/by_level/', { params: { level: levelCode } }),
  getLessons: (unitId) =>
    apiClient.get('lessons/', { params: { unit: unitId } }),
  getExercises: (lessonId, skillCode) =>
    apiClient.get('exercises/by_lesson/', { params: { lesson: lessonId, skill: skillCode } }),
  getExerciseDetail: (id) =>
    apiClient.get(`exercises/${id}/`),
  submitExercise: (id, answer, timeSpent) =>
    apiClient.post(`exercises/${id}/submit/`, { answer, time_spent_seconds: timeSpent }),
  getVocabulary: (lessonId) =>
    apiClient.get('vocabulary/', { params: { lesson: lessonId } }),
  getDialogues: (lessonId) =>
    apiClient.get('dialogues/', { params: { lesson: lessonId } }),
  getGames: (lessonId) =>
    apiClient.get('games/', { params: { lesson: lessonId } }),
  getGameDetail: (id) =>
    apiClient.get(`games/${id}/`),
  submitGame: (id, score, timeSpent) =>
    apiClient.post(`games/${id}/submit/`, { score, time_spent_seconds: timeSpent }),
}

export const progressAPI = {
  getProgress: () =>
    apiClient.get('progress/my_progress/'),
  getProgressByLevel: (levelCode) =>
    apiClient.get('progress/by_level/', { params: { level: levelCode } }),
  getBadges: () =>
    apiClient.get('badges/my_badges/'),
  checkAchievements: () =>
    apiClient.post('badges/check_achievements/'),
  getReviewItems: () =>
    apiClient.get('review/due_for_review/'),
  markReviewCorrect: (id) =>
    apiClient.post(`review/${id}/mark_correct/`),
  markReviewIncorrect: (id) =>
    apiClient.post(`review/${id}/mark_incorrect/`),
}

export const profileAPI = {
  getProfile: () =>
    apiClient.get('profiles/my_profile/'),
  updateLevel: (level) =>
    apiClient.post('profiles/update_level/', { level }),
}

export default apiClient
