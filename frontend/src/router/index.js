import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

// Pages
import LoginPage from '../pages/LoginPage.vue'
import FirstPasswordChangePage from '../pages/FirstPasswordChangePage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import LevelPage from '../pages/LevelPage.vue'
import UnitListPage from '../pages/UnitListPage.vue'
import LessonPage from '../pages/LessonPage.vue'
import ExercisePage from '../pages/ExercisePage.vue'
import GamePlayPage from '../pages/GamePlayPage.vue'
import MyProgressPage from '../pages/MyProgressPage.vue'
import ReviewPage from '../pages/ReviewPage.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/first-password-change',
    name: 'FirstPasswordChange',
    component: FirstPasswordChangePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/levels',
    name: 'Levels',
    component: LevelPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/level/:levelCode/units',
    name: 'UnitList',
    component: UnitListPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/unit/:unitId/lessons',
    name: 'Lessons',
    component: LessonPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/lesson/:lessonId/exercises',
    name: 'Exercises',
    component: ExercisePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/exercise/:exerciseId',
    name: 'ExercisePlay',
    component: ExercisePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/game/:gameId',
    name: 'GamePlay',
    component: GamePlayPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/progress',
    name: 'MyProgress',
    component: MyProgressPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/review',
    name: 'Review',
    component: ReviewPage,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth === false) {
    // Public pages
    if (authStore.isAuthenticated) {
      next('/dashboard')
    } else {
      next()
    }
  } else if (to.meta.requiresAuth) {
    // Protected pages
    if (!authStore.isAuthenticated) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
