<template>
  <div class="container-main">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Lessons</h1>
    
    <div v-if="exerciseStore.isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading lessons...</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <router-link
        v-for="lesson in exerciseStore.lessons"
        :key="lesson.id"
        :to="`/lesson/${lesson.id}/exercises`"
        class="card hover:shadow-xl cursor-pointer"
      >
        <h3 class="text-xl font-bold text-gray-900">{{ lesson.title }}</h3>
        <p class="text-gray-600 mt-2">{{ lesson.objective }}</p>
        <div v-if="lesson.vocabulary_focus" class="mt-3 text-sm text-gray-500">
          📝 {{ lesson.vocabulary_focus }}
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useExerciseStore } from '../stores/exerciseStore'

const route = useRoute()
const exerciseStore = useExerciseStore()

onMounted(() => {
  exerciseStore.fetchLessons(route.params.unitId)
})
</script>
