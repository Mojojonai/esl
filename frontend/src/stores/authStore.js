import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('authToken') || null)
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_staff || false)

  const setAuthData = (newToken, newUser, profileData = null) => {
    token.value = newToken
    user.value = profileData ? { ...newUser, profile: profileData } : newUser
    localStorage.setItem('authToken', newToken)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
  }

  const checkAuthStatus = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser && token.value) {
      user.value = JSON.parse(savedUser)
    }
  }

  const login = async (username, password) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await authAPI.login(username, password)
      const { token: newToken, user: newUser, profile: profileData } = response.data
      setAuthData(newToken, newUser, profileData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await authAPI.logout()
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      clearAuth()
    }
  }

  const changePassword = async (oldPassword, newPassword) => {
    isLoading.value = true
    error.value = null
    try {
      await authAPI.changePassword(oldPassword, newPassword)
      return true
    } catch (err) {
      error.value = err.response?.data || 'Password change failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    setAuthData,
    clearAuth,
    checkAuthStatus,
    login,
    logout,
    changePassword,
  }
})
